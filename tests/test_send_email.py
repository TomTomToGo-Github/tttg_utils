## built-in modules
import os
import time
from pathlib import Path
# import pytest
# from unittest.mock import patch
## pip installed modules
from dotenv import load_dotenv
## self-made modules
from tttg_utils.automation.email import send_email


load_dotenv()

# @patch('tttg_utils.automation.email.send_email')
def test_send_email():  # mock_send_email):
    browser_name = 'edge'  # 'edge' or 'chrome'
    browser_driver_path = Path(os.getenv('PATH_BROWSER_DRIVERS'))
    headless = False
    # Arrange
    sender_email = os.getenv('THAID_GMX_EMAIL')
    receiver_email = os.getenv('THAID_GMX_EMAIL')
    message = 'Test message'

    # Act
    driver = send_email(
        sender_email,
        receiver_email,
        message, 
        provider_url=os.getenv('THAID_GMX_URL'),
        sender_pwd=os.getenv('THAID_GMX_PWD'),
        browser_name=browser_name,
        browser_driver_path=browser_driver_path,
        headless=headless
    )
    
    # from selenium.webdriver.common.by import By
    # save_html_from_url(driver, 'test.html')
    # ids = driver.find_element(by="xpath", value="//.")
    # html = driver.page_source
    # time.sleep(2)
    # print(html)
    # ids = driver.find_elements_by_xpath('//*[@id=*]')
    # for ii in ids:
    #     print(ii.get_attribute('id'))
    # # Assert
    # mock_send_email.assert_called_once_with(to_email, subject, body)