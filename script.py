from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF
from PIL import Image
import time
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "http://e-books.helwan.edu.eg/storage/20228/index.html#/reader/chapter/"
total_pages = 260
start_page = 4
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def take_screenshot(page_number):
    url = f"{base_url}{page_number}"
    driver.get(url)
    time.sleep(5)
    try:
        screenshot_path = os.path.join(screenshot_dir, f"page_{page_number}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved for page {page_number}")
        return screenshot_path
    except Exception as e:
        print(f"Failed to take screenshot of page {page_number}: {str(e)}")
        return None

def create_pdf_from_images(image_paths):
    pdf = FPDF(unit="mm", format="A4")
    
    for image_path in image_paths:
        image = Image.open(image_path)
        width, height = image.size
        pdf.add_page()
        max_width = 210
        max_height = 297
        scale_ratio = min( (max_width / (width * 0.264583)) , (max_height / (height * 0.264583)) )
        scaled_width = width * 0.264583 * scale_ratio
        scaled_height = height * 0.264583 * scale_ratio
        x_offset = (max_width - scaled_width) / 2
        y_offset = (max_height - scaled_height) / 2
        pdf.image(image_path, x=x_offset, y=y_offset, w=scaled_width, h=scaled_height)
    
    pdf.output("pages_screenshots.pdf")
    print("PDF created from screenshots successfully!")

image_paths = []
for i in range(start_page, total_pages + 1):
    screenshot_path = take_screenshot(i)
    image_paths.append(screenshot_path)

create_pdf_from_images(image_paths)
driver.quit()
