import os

# Get the directory of the current config file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#CHROME_USER_DATA_DIR = r"C:\Users\imsur\AppData\Local\Google\Chrome\User Data" #use the correct path
CHROME_USER_DATA_DIR = os.path.expanduser("~/.config/google-chrome/User Data")
CHROME_PROFILE_NAME = "Whatsapp"  # Specify the profile you want to use
#DRIVER_PATH = "C:\\Users\\Administrator\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Use the correct path

# Data files
DAY_PLACE_MAPPING_FILE_PATH = os.path.join(ROOT_DIR, "Data", "day_place_mapping.xlsx")
DATA_FILE_PATH_ENGLISH = os.path.join(ROOT_DIR, "Data", "place_with_facts_eng.xlsx")
DATA_FILE_PATH_TAMIL = os.path.join(ROOT_DIR, "Data", "place_with_facts_tam.xlsx")

# Messages
MESSAGE_FILE = os.path.join(ROOT_DIR, "msg.txt")
GROUPS_FILE = os.path.join(ROOT_DIR, "groups.txt") # Assuming groups.txt is also in the root
GROUP_NAME = os.path.join(ROOT_DIR, "group_name.txt")
IMAGE_FILE = os.path.join(ROOT_DIR, "Images")

# Gmail related
SENDER_EMAIL = "violentstudioz@gmail.com"  # Replace with your email address
SENDER_PASSWORD = "nevr qgeo qvqd yszp"  # Replace with your email password
RECEIVER_EMAIL = "zications@gmail.com" # Replace with your email address
