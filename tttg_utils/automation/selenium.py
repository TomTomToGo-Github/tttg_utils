## built-in modules
import os
import time
from pathlib import Path
## pip installed modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService


def setup_driver(browser_name, browser_driver_path, headless=None, url=None):
    """Helper function to setup the webdriver."""
    if browser_name == 'chrome':
        driver_exe = 'chromedriver_win64_v119.exe'
        s = ChromeService(browser_driver_path / driver_exe)
    elif browser_name == 'edge':
        driver_exe = 'msedgedriver_win64_v118.exe'
        s = EdgeService(browser_driver_path / driver_exe)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    options = webdriver.ChromeOptions() if browser_name == 'chrome' else webdriver.EdgeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(service=s, options=options) if browser_name == 'chrome' else webdriver.Edge(service=s, options=options)
    if url:
        driver.get(url)
    return driver

def save_html_from_url(driver, html_file_name, html_path=None):
    html_file_name = Path(html_file_name)
    if not html_path:
        html_path = Path(os.getcwd())
    html_path = Path(html_path)
    html = driver.page_source
    time.sleep(2)
    if str(html_file_name.parent) == '.':
        html_path_file = html_path / "{}.html".format(html_file_name.stem)
    else:
        html_path_file = html_path / html_file_name.parent / "{}.html".format(html_file_name.stem)
    if not html_path_file.perent.is_dir():
        html_path_file.mkdir(parents=True)
    with open(html_path_file, 'w') as f:
        f.write(html)
    # print(html)
    
def save_complete_screenshot(driver: webdriver.Chrome, path: str = '/tmp/screenshot.png', headless=False) -> None:
    nap_time = .5
    ## Set window size
    if not headless:
        time.sleep(nap_time)
    original_size = driver.get_window_size()
    driver.maximize_window()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    if not headless:
        time.sleep(nap_time)
    driver.find_element(By.TAG_NAME, "body").screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])
    if not headless:
        time.sleep(nap_time)

def save_html_to_png(html_file_name, html_path=None, browser_name=None, browser_driver_path=None, headless=False):
    """Converts an HTML file to a PNG image using Selenium.

    Args:
        html_file_name: The name of the HTML file to convert.
        html_path: The directory of the HTML file. Defaults to the current working directory.
        browser_name: The name of the browser to use. Defaults to "edge".
        browser_driver_path: The path to the browser driver. Defaults to a subdirectory 'browser_drivers' in the current working directory.
        headless: Whether to run the browser in headless mode. Defaults to False.

    Raises:
        FileNotFoundError: If the HTML file or the browser driver is not found.
        Exception: If the browser fails to launch.
    """
    if html_path:
        html_path = Path(html_path)
    else:
        html_path = Path(os.getcwd())
    html_file_name = Path(html_file_name)

    if not browser_name:
        browser_name = "edge"

    if not browser_driver_path:
        browser_driver_path = Path(os.getcwd()) / 'browser_drivers'

    driver = setup_driver(browser_name, browser_driver_path, headless)

    file_url = f'file:///{(html_path / html_file_name.stem)}.html'
    png_path_file = f'{(html_path / html_file_name.stem)}.png'
    driver.get(file_url)
    save_complete_screenshot(driver=driver, path=png_path_file, headless=headless)
    driver.quit()
    return png_path_file
