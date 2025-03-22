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
import pyperclip
import time
import sys
import send_mail
from datetime import datetime
from config import (CHROME_USER_DATA_DIR, CHROME_PROFILE_NAME, IMAGE_FILE, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)

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


# --- Headless Mode Configuration ---
options = Options()
options.add_argument("--headless")

options.add_argument("--no-sandbox")

options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.binary_location = '/usr/bin/google-chrome' # Explicitly set Chromium location
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
# --- End of Headless Mode Configuration ---



# Initialize Chrome webdriver

try:

#    service = Service('/usr/bin/chromedriver') # Explicitly set ChromeDriver location
    service = Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(service = service,  options=options)

except Exception as e:

    print(f"Error initializing ChromeDriver with explicit path: {e}")

    try:

        browser = webdriver.Chrome(options=options) # Try without explicit service

    except Exception as e2:

        print(f"Error initializing ChromeDriver without Service: {e2}")

        try:

            service = Service(ChromeDriverManager().install()) # Try with webdriver-manager

            browser = webdriver.Chrome(service=service, options=options)

        except Exception as e3:

            print(f"Error initializing ChromeDriver with ChromeDriverManager: {e3}")

            raise

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
        #qr_code_element = browser.find_element(By.XPATH, '//div[@data-ref]') # Example
        print("QR code element found. Taking screenshot and sending email...")
        browser.save_screenshot(SCREENSHOT_PATH)
        send_mail.send_email_with_screenshot(SCREENSHOT_PATH) # Call the function from the imported script
        print(f"Screenshot saved to {SCREENSHOT_PATH} and email sent to {RECEIVER_EMAIL}")

        wait_time_seconds = 120  # Wait for 2 minutes (adjust as needed)
        print(f"Waiting for {wait_time_seconds} seconds for you to scan the QR code from the email...")
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
    time.sleep(2)
    search_box.send_keys(Keys.CONTROL + Keys.SHIFT +  "v")  # Keys.CONTROL + "v"
    
    print(f"Pasted the group name in the search box successfully")
    time.sleep(2)
    
    wait = WebDriverWait(browser, 10)  # Wait for a maximum of 10 seconds
    group_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@title="Test"]')))
    group_element.click()
    
    time.sleep(1)

    #input_xpath = '//div[@contenteditable="true"][@data-tab="10"][@aria-placeholder="Type an update"]'
    #input_box = browser.find_element(By.XPATH, input_xpath)
    
    #input_box.click()
    

    #input_box.send_keys(Keys.SHIFT + Keys.INSERT)  # Keys.CONTROL + "v"

    #input_box.send_keys(Keys.ENTER)

    #time.sleep(5)
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
        if 1==1:
            attachment_box = browser.find_element(By.XPATH,'//button[@title="Attach"]')
            attachment_box.click()
            time.sleep(1)
            image_path = f'{IMAGE_FILE}/{place_name}.jpeg'

            image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(image_path)
            time.sleep(2)
         #   image_box.send_keys(Keys.ENTER)

            send_btn = browser.find_element(By.XPATH,'//div[@role="button"][@aria-label="Send"]')
            send_btn.click()
            time.sleep(4)

    except IndexError:
        pass
