import os

# Get the directory of the current config file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CHROME_USER_DATA_DIR = r"C:\Users\RAJCHINN SATHISH\AppData\Local\Google\Chrome\User Data" #use the correct path
CHROME_PROFILE_NAME = "Profile 16"  # Specify the profile you want to use
DRIVER_PATH = "C:\\Users\\RAJCHINN SATHISH\\Downloads\\chromedriver-win64\\chromedriver.exe"  # Use the correct path

# Data files
DAY_PLACE_MAPPING_FILE_PATH = os.path.join(ROOT_DIR, "Data", "day_place_mapping.xlsx")
DATA_FILE_PATH = os.path.join(ROOT_DIR, "Data", "place_with_facts.xlsx")

# Messages
MESSAGE_FILE = os.path.join(ROOT_DIR, "msg.txt")
GROUPS_FILE = os.path.join(ROOT_DIR, "groups.txt") # Assuming groups.txt is also in the root