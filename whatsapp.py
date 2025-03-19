from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyperclip
import time
import sys
from config import (CHROME_USER_DATA_DIR, CHROME_PROFILE_NAME, DRIVER_PATH)

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
chrome_options.add_argument(f"user-data-dir={CHROME_USER_DATA_DIR}")  # Path to your user data
chrome_options.add_argument(f"profile-directory={CHROME_PROFILE_NAME}")  # Specify the profile you want to use

# Create a Service object
service = Service(DRIVER_PATH)

image_path = f'C:\\Users\\RAJCHINN SATHISH\\Desktop\\Zi\\Images\\{place_name}.jpg'


# Initialize the WebDriver with the Service object and Chrome options
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.maximize_window()

browser.get('https://web.whatsapp.com/')

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
            image_path = f'C:\\Users\\RAJCHINN SATHISH\\Desktop\\Zi\\Images\\{place_name}.jpeg'

            image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(image_path)
            time.sleep(2)
         #   image_box.send_keys(Keys.ENTER)

            send_btn = browser.find_element(By.XPATH,'//div[@role="button"][@aria-label="Send"]')
            send_btn.click()
            time.sleep(4)

    except IndexError:
        pass