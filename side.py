from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import sys
from config import CHROME_PROFILE_PATH

CHROME_USER_DATA_DIR = r"C:\Users\RAJCHINN SATHISH\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Profile 16"  # Specify the profile you want to use


with open('msg.txt', 'r', encoding='utf8') as f:
    msg = f.read()

with open('groups.txt', 'r', encoding='utf8') as f:
    groups = f.readlines()
	

try:
        browser = await launch(
            headless=False,  # Set to True if you don't want to see the browser UI
            user_data_dir=CHROME_USER_DATA_DIR,
            args=[f'--profile-directory={CHROME_PROFILE_NAME}'],	
            executablePath="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Replace with your actual Chrome path

        )
        pages = await browser.pages()
        page = pages[0] if pages else await browser.newPage()

browser.get('https://web.whatsapp.com/')


for group in groups:
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

    search_box = WebDriverWait(browser, 500).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )

    search_box.clear()

    time.sleep(1)

    pyperclip.copy(group)

    search_box.send_keys(Keys.CONTROL + "v")  # Keys.CONTROL + "v"

    time.sleep(2)

    group_xpath = f'//span[@title="{group}"]'
    group_title = browser.find_element(By.XPATH, group_xpath)

    group_title.click()

    time.sleep(1)

    input_xpath = '//div[@contenteditable="true"][@data-tab="10"][@aria-placeholder="Type a message"]'
    input_box = browser.find_element(By.XPATH, input_xpath)
    input_box.click()

    pyperclip.copy(msg)

    input_box.send_keys(Keys.CONTROL + "v")  # Keys.CONTROL + "v"

    #input_box.send_keys(Keys.ENTER)

    time.sleep(5)

    try:
        if 1==1:
            attachment_box = browser.find_element(By.XPATH,'//button[@title="Attach"]')
            attachment_box.click()
            time.sleep(1)
            image_path = 'C:\\Users\\RAJCHINN SATHISH\\Desktop\\Zi\\jyothi.jpg'

            image_box = browser.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(image_path)
            time.sleep(2)
         #   image_box.send_keys(Keys.ENTER)

            send_btn = browser.find_element(By.XPATH,'//div[@role="button"][@aria-label="Send"]')
            send_btn.click()
            time.sleep(4)

    except IndexError:
        pass