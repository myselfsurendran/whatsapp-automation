from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import sys
import send_mail
from datetime import datetime
from config import (CHROME_USER_DATA_DIR, IMAGE_FILE, RECEIVER_EMAIL)

SCREENSHOT_PATH = "qr_code.png"

if len(sys.argv) > 1:
    place_name = sys.argv[1]
    print(f"Received place name: {place_name}")
else:
    print("Error: Place name not provided.")
    sys.exit(1)

with open('whatsapp-automation/msg.txt', 'r', encoding='utf8') as f:
    msg = f.read()

with open('whatsapp-automation/group_name.txt', 'r', encoding='utf8') as f:
    groups = [line.strip() for line in f.readlines()]


# --- Headless Mode Configuration ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.binary_location = '/usr/bin/google-chrome'
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
# --- End of Headless Mode Configuration ---

# Initialize Chrome webdriver
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

browser.maximize_window()
browser.get('https://web.whatsapp.com/')

time.sleep(10)

try:
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )
    print("WhatsApp Web loaded successfully (likely logged in).")

except Exception as e:
    print("Could not find the logged-in indicator. Checking for QR code...")
    try:
        print("QR code element found. Taking screenshot and sending email...")
        browser.save_screenshot(SCREENSHOT_PATH)
        send_mail.send_email_with_screenshot(SCREENSHOT_PATH)
        print(f"Screenshot saved to {SCREENSHOT_PATH} and email sent to {RECEIVER_EMAIL}")

        wait_time_seconds = 120  
        print(f"Waiting for {wait_time_seconds} seconds for you to scan the QR code scan...")
        time.sleep(wait_time_seconds)

    except Exception as e_qr:
        print(f"QR code element not found. Error: {e_qr}")

time.sleep(5)

for group in groups:
    channel_xpath = '//span[@aria-hidden="true"][@data-icon="newsletter-outline"]'
    channel = browser.find_element(By.XPATH, channel_xpath)
    channel.click()
    print("Channel page went successfully")

    time.sleep(1)

    search_path = '//div[@contenteditable="true"][@data-tab="3"]'
    search_box = browser.find_element(By.XPATH, search_path)
    search_box.clear()

    print("Search box cleared successfully")
    time.sleep(1)

    #pyperclip.copy(group)
    search_box.click()
    time.sleep(1)

    search_box.send_keys(group)
    print(f"Typed the group name in the search box successfully")

    time.sleep(2)

    all_spans = browser.find_elements(By.XPATH, '//span')
    print("Available span texts:")
    for span in all_spans:
        print(repr(span.text))  # Print exactly what WhatsApp Web shows

    wait = WebDriverWait(browser, 20)  
    group_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{group.strip()}")]')))
    group_element.click()

    time.sleep(1)

    input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
    input_box = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, input_xpath))
    )
    
    actions = ActionChains(browser)
    actions.move_to_element(input_box).click().perform()
    time.sleep(2)

    browser.execute_cdp_cmd('Input.insertText', {'text': msg})

    time.sleep(2)
    try:
        attachment_box = browser.find_element(By.XPATH,'//button[@title="Attach"]')
        attachment_box.click()
        time.sleep(1)

        image_path = f'{IMAGE_FILE}/{place_name}.jpg'
        image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
        image_box.send_keys(image_path)

        time.sleep(2)

        send_btn = browser.find_element(By.XPATH,'//div[@role="button"][@aria-label="Send"]')
        time.sleep(4)
        send_btn.click()
        time.sleep(4)

    except Exception as e:
        print(f"Attachment or send error: {e}")


browser.quit()
