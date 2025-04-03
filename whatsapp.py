from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import send_mail
from config import (CHROME_USER_DATA_DIR, IMAGE_FILE, RECEIVER_EMAIL)

def capture_and_notify(error_message):
    screenshot_file = "error_screenshot.png"
    browser.save_screenshot(screenshot_file)
    send_mail.send_email_with_screenshot(screenshot_file)
    print(f"Error: {error_message}. Screenshot saved and email sent.")

if len(sys.argv) > 1:
    place_name = sys.argv[1]
else:
    print("Error: Place name not provided.")
    sys.exit(1)

try:
    with open('whatsapp-automation/msg.txt', 'r', encoding='utf8') as f:
        msg = f.read()
    with open('whatsapp-automation/group_name.txt', 'r', encoding='utf8') as f:
        groups = [line.strip() for line in f.readlines()]
except Exception as e:
    print(f"Error reading files: {e}")
    sys.exit(1)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
service = Service(ChromeDriverManager().install())

try:
    browser = webdriver.Chrome(service=service, options=options)
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')
    time.sleep(10)
except Exception as e:
    capture_and_notify(f"Browser initialization failed: {e}")
    sys.exit(1)

try:
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    print("WhatsApp Web loaded successfully.")
except Exception:
    capture_and_notify("Could not detect WhatsApp Web login.")
    sys.exit(1)

time.sleep(5)

for group in groups:
    try:
        channel_xpath = '//span[@aria-hidden="true"][@data-icon="newsletter-outline"]'
        channel = browser.find_element(By.XPATH, channel_xpath)
        channel.click()
        print("Navigated to the channel page.")
        time.sleep(1)
    except Exception:
        capture_and_notify("Failed to open the channel page.")
        continue


    try:
        wait = WebDriverWait(browser, 20)
        group_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{group.strip()}")]')))
        group_element.click()
        time.sleep(1)
    except Exception:
        capture_and_notify(f"Failed to find or select group: {group}")
        continue

    try:
        input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        input_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
        actions = ActionChains(browser)
        actions.move_to_element(input_box).click().perform()
        time.sleep(2)
        browser.execute_cdp_cmd('Input.insertText', {'text': msg})
        time.sleep(2)
    except Exception:
        capture_and_notify("Failed to send message.")
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
    except Exception:
        capture_and_notify("Failed to send image attachment.")
        continue

browser.quit()
