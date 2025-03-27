import pandas as pd
#import schedule
from datetime import datetime
import subprocess
from config import (
    DATA_FILE_PATH,
    MESSAGE_FILE,
    DAY_PLACE_MAPPING_FILE_PATH 
)

def get_place_for_today():
    today_date = datetime.now().strftime('%Y-%m-%d')
    try:
        mapping_df = pd.read_excel(DAY_PLACE_MAPPING_FILE_PATH)  
        print(mapping_df)
        place_row = mapping_df[mapping_df['Date'] == today_date] 
        print(place_row )
        if not place_row.empty:
            return place_row['Place Name'].iloc[0] 
        else:
            print(f"No place found for date: {today_date} in the mapping sheet.")
            return None

    except FileNotFoundError:
        print(f"Error: Day mapping file '{DAY_PLACE_MAPPING_FILE_PATH}' not found.")
        return None

    except Exception as e:
        print(f"An error occurred while reading the mapping sheet: {e}")
        return None

def process_and_send_data():
    place_name = get_place_for_today()
    if not place_name:
        return

    try:
        df = pd.read_excel(DATA_FILE_PATH) 

        place_data = df[df.iloc[:, 0] == place_name].iloc[:, 1].iloc[0]

        print(f"Data found for {place_name}: {place_data}")

        with open(MESSAGE_FILE, 'w', encoding='utf8') as f:
            f.write(place_data)

        print("Data written to msg.txt")

        subprocess.run(['python3', 'whatsapp-automation/whatsapp_script.py', place_name])
        
        print("WhatsApp automation script triggered.")

    except FileNotFoundError:
        print(f"Error: Data file '{DATA_FILE_PATH}' not found.")
    except KeyError:
        print(f"Error: Place '{place_name}' not found in the data.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_and_send_data()
    print("Script execution finished.")
