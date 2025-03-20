from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import pyperclip
import time
import sys
import send_mail
from config import (CHROME_USER_DATA_DIR, CHROME_PROFILE_NAME, DRIVER_PATH, IMAGE_FILE, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)

SCREENSHOT_PATH = "qr_code.png"

if len(sys.argv) > 1:
    place_name = sys.argv[1]
    print(f"Received place name in WhatsApp script: {place_name}")
else:
    print("Error: Place name not provided as a command-line argument.")
    sys.exit(1)

with open('msg.txt', 'r', encoding='utf8') as f:
    msg = f.read()

with open('groups.txt', 'r', encoding='utf8') as f:
    groups = f.readlines()


chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={CHROMEDRIVER_PATH}")  # Path to your user data
chrome_options.add_argument(f"profile-directory={CHROME_PROFILE_NAME}")  # Specify the profile you want to use

chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create a Service object
service = Service(DRIVER_PATH)

# Initialize the WebDriver with the Service object and Chrome options
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.maximize_window()

browser.get('https://web.whatsapp.com/')

time.sleep(10)

try:
    # Try to find an element that indicates the user is logged in (e.g., the search box)
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )
    print("WhatsApp Web loaded successfully (likely logged in).")

except Exception as e:
    print("Could not find the logged-in indicator. Checking for QR code...")
    try:
        # Look for an element specific to the QR code page (adjust the selector)
        qr_code_element = browser.find_element(By.XPATH, '//div[@data-ref]') # Example
        print("QR code element found. Taking screenshot and sending email...")
        browser.save_screenshot(SCREENSHOT_PATH)
        send_mail.send_email_with_screenshot(SCREENSHOT_PATH) # Call the function from the imported script
        print(f"Screenshot saved to {SCREENSHOT_PATH} and email sent to {RECEIVER_EMAIL}")

        wait_time_seconds = 120  # Wait for 2 minutes (adjust as needed)
        print(f"Waiting for {wait_time_seconds} seconds for you to scan the QR code from the email...")
        time.sleep(wait_time_seconds)

    except Exception as e_qr:
        print(f"QR code element not found. Error: {e_qr}")

time.sleep(10)


for group in groups:
    channel_xpath = '//span[@aria-hidden="true"][@data-icon="newsletter-outline"]'

    channel = browser.find_element(By.XPATH, channel_xpath)

    channel.click()

    time.sleep(1)

    search_path = '//div[@contenteditable="true"][@data-tab="3"]'
    search_box = browser.find_element(By.XPATH, search_path)
    search_box.clear()

    time.sleep(1)

    pyperclip.copy(group)
    search_box.send_keys(Keys.CONTROL + "v")  # Keys.CONTROL + "v"

    time.sleep(2)

    group_xpath = f'//span[@title="{group}"]'
    group_title = browser.find_element(By.XPATH, group_xpath)

    group_title.click()

    time.sleep(1)

    input_xpath = '//div[@contenteditable="true"][@data-tab="10"][@aria-placeholder="Type an update"]'
    input_box = browser.find_element(By.XPATH, input_xpath)
    input_box.clear()

    #input_box.click()

    pyperclip.copy(msg)
    input_box.send_keys(Keys.CONTROL + "v")  # Keys.CONTROL + "v"

    #input_box.send_keys(Keys.ENTER)

    time.sleep(5)

    try:
        if 1==1:
            attachment_box = browser.find_element(By.XPATH,'//button[@title="Attach"]')
            attachment_box.click()
            time.sleep(1)
            image_path = f'{IMAGE_FILE}\\{place_name}.jpeg'

            image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(image_path)
            time.sleep(2)
         #   image_box.send_keys(Keys.ENTER)

            send_btn = browser.find_element(By.XPATH,'//div[@role="button"][@aria-label="Send"]')
            send_btn.click()
            time.sleep(4)

    except IndexError:
        pass
