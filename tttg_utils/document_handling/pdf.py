## built-in modules
import os
from pathlib import Path
from datetime import datetime
## pip installed modules
from PIL import Image, ImageOps
import img2pdf


def ensure_folder_structure(project_name='state_2023_07_11', folder_base=None):
    folder_base = Path(folder_base or os.getcwd())
    ## define folder structure
    data_time_now = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    folder_load_tests =  folder_base / 'load_tests'
    folder_project = f'wooo_postman_environment_{project_name}'
    folder_results = folder_load_tests / folder_project / f'load_tests_{data_time_now}'
    folder_results.mkdir(parents=True, exist_ok=True)
    return folder_results

# Open the image file
def img_to_pdf(file, fit_option='A4_width', border_width=(0, 0, 0, 0), save_resized=False):
    # file = "stats_output.png"
    filename = Path(file)
    resized_file = filename.parent / f"resized_{filename.stem}.png"
    pdf_file = filename.parent / f"{filename.stem}.pdf"
    with Image.open(filename) as img:
        # Resize the image
        width_old, height_old = img.size
        if fit_option == 'A4':
            width_new = 2480
            height_new = 3508
        elif fit_option == 'A4_width':
            width_new = 2480
            height_new = round(height_old * 2480 / width_old)
        elif fit_option == 'A4_height':
            height_new = 3508
            width_new = round(width_old * 3508 / height_old)
        else:
             width_new, height_new = width_old, height_old
        # Resize the image to selected fit option
        img = img.resize((width_new - border_width[0] - border_width[2], height_new - border_width[1] - border_width[3]))  # Resize to half of the original size
        border_color = (255, 255, 255)  # White
        img = ImageOps.expand(img, border=border_width, fill=border_color)
        # Save the resized image
        img.save(resized_file)
    # Convert the resized image to PDF
    pdf_file.write_bytes(img2pdf.convert(resized_file))
    if not save_resized:
        resized_file.unlink()
