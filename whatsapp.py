from selenium import webdriver
from selenium.webdriver.common.by import By
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
    try:
        browser.save_screenshot(SCREENSHOT_PATH)
        print(f"Screenshot saved at {SCREENSHOT_PATH}")
        send_mail.send_email_with_screenshot(SCREENSHOT_PATH)
        print("Error notification email sent.")
    except Exception as e:
        print(f"Failed to capture screenshot or send email: {e}")

try:
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

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.maximize_window()

    try:
        browser.get('https://web.whatsapp.com/')
        time.sleep(10)
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )
        print("WhatsApp Web loaded successfully.")
    except Exception as e:
        print("WhatsApp Web did not load correctly.")
        capture_and_notify(f"Failed to load WhatsApp Web: {e}")
        browser.quit()
        sys.exit(1)

    for group in groups:
        try:
            search_path = '//div[@contenteditable="true"][@data-tab="3"]'
            search_box = browser.find_element(By.XPATH, search_path)
            search_box.clear()
            search_box.send_keys(group)
            print(f"Typed group name: {group}")
            time.sleep(2)

            wait = WebDriverWait(browser, 20)
            group_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{group}")]')))
            group_element.click()
            print(f"Successfully found and selected group: {group}")
        except Exception as e:
            print(f"Failed to find or select group: {group}")
            capture_and_notify(f"Failed to find or select group: {e}")
            continue

        try:
            input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
            input_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, input_xpath))
            )
            actions = ActionChains(browser)
            actions.move_to_element(input_box).click().perform()
            time.sleep(2)

            browser.execute_cdp_cmd('Input.insertText', {'text': msg})
            print("Message inserted into chat successfully.")
        except Exception as e:
            print("Failed to type the message.")
            capture_and_notify(f"Failed to type message: {e}")
            continue

        try:
            attachment_box = browser.find_element(By.XPATH, '//button[@title="Attach"]')
            attachment_box.click()
            time.sleep(1)

            image_path = f'{IMAGE_FILE}/{place_name}.jpg'
            image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(image_path)
            time.sleep(2)

            send_btn = browser.find_element(By.XPATH, '//div[@role="button"][@aria-label="Send"]')
            time.sleep(4)
            send_btn.click()
            time.sleep(4)
            print("Image sent successfully.")
        except Exception as e:
            print("Failed to send image.")
            capture_and_notify(f"Failed to send image: {e}")
            continue

finally:
    browser.quit()
    print("Browser session ended.")
