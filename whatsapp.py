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

SCREENSHOT_PATH = "error_screenshot.png"

def capture_and_notify(error_message):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = f"error_{timestamp}.png"
    browser.save_screenshot(screenshot_file)
    send_mail.send_email_with_screenshot(screenshot_file, error_message)
    print(f"Error: {error_message}. Screenshot saved and email sent.")

if len(sys.argv) > 1:
    place_name = sys.argv[1]
    print(f"Received place name: {place_name}")
else:
    print("Error: Place name not provided.")
    sys.exit(1)

try:
    with open('whatsapp-automation/msg.txt', 'r', encoding='utf8') as f:
        msg = f.read()
except Exception as e:
    capture_and_notify(f"Failed to read message file: {e}")
    sys.exit(1)

try:
    with open('whatsapp-automation/group_name.txt', 'r', encoding='utf8') as f:
        groups = [line.strip() for line in f.readlines()]
except Exception as e:
    capture_and_notify(f"Failed to read group names file: {e}")
    sys.exit(1)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.binary_location = '/usr/bin/google-chrome'
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")

try:
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')
    time.sleep(10)
except Exception as e:
    capture_and_notify(f"Failed to initialize browser: {e}")
    sys.exit(1)

try:
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )
    print("WhatsApp Web loaded successfully (likely logged in).")
except Exception as e:
    capture_and_notify(f"Could not find WhatsApp Web login: {e}")
    sys.exit(1)

time.sleep(5)

for group in groups:
    try:
        channel_xpath = '//span[@aria-hidden="true"][@data-icon="newsletter-outline"]'
        channel = browser.find_element(By.XPATH, channel_xpath)
        channel.click()
        print("Channel page opened successfully.")
    except Exception as e:
        capture_and_notify(f"Failed to open channel page: {e}")
        continue

    time.sleep(1)
    try:
        search_path = '//div[@contenteditable="true"][@data-tab="3"]'
        search_box = browser.find_element(By.XPATH, search_path)
        search_box.clear()
        search_box.send_keys(group)
        print(f"Searching for group: {group}")
    except Exception as e:
        capture_and_notify(f"Failed to search for group: {e}")
        continue

    time.sleep(2)
    try:
        group_xpath = f'//span[contains(text(), "{group}")]'
        group_element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, group_xpath))
        )
        group_element.click()
        print(f"Successfully selected group: {group}")
    except Exception as e:
        capture_and_notify(f"Failed to find or select group: {e}")
        continue

    time.sleep(1)
    try:
        input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        input_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, input_xpath))
        )
        actions = ActionChains(browser)
        actions.move_to_element(input_box).click().perform()
        time.sleep(2)
        browser.execute_cdp_cmd('Input.insertText', {'text': msg})
        print("Message entered successfully.")
    except Exception as e:
        capture_and_notify(f"Failed to enter message: {e}")
        continue

    time.sleep(2)
    try:
        attachment_box = browser.find_element(By.XPATH, '//button[@title="Attach"]')
        attachment_box.click()
        time.sleep(1)
        image_path = f'{IMAGE_FILE}/{place_name}.jpg'
        image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
        image_box.send_keys(image_path)
        time.sleep(2)
        send_btn = browser.find_element(By.XPATH, '//div[@role="button"][@aria-label="Send"]')
        send_btn.click()
        print("Image sent successfully.")
    except Exception as e:
        capture_and_notify(f"Failed to send image: {e}")
        continue

time.sleep(5)
browser.quit()
print("Script execution completed.")
