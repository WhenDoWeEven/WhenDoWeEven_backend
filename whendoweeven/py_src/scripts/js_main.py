import json
import sys
from pathlib import Path
import argparse
from datetime import datetime, time
from pymongo import MongoClient

from cal_parser.convert import convert_user_json_calendar_to_ics


def get_user_json_calendar(user_json_cal: json) -> dict:
    # user_dict_cal = convert_user_json_calendar_to_dict(user_json_cal)
    user_ics_cal = convert_user_json_calendar_to_ics(user_json_cal)


def get_user_google_calendar(user_google_cal:json) -> dict:
    
    # user_dict_cal = convert_user_json_calendar_to_dict(user_google_cal)
    user_ics_cal = convert_user_json_calendar_to_ics(user_google_cal)

def get_user_apple_calendar(user_apple_cal:json) -> dict:
    # user_dict_cal = convert_user_json_calendar_to_dict(user_apple_cal)
    user_ics_cal = convert_user_json_calendar_to_ics()



def delete_temp_json_file(file_path: str)-> bool:
    try:
        file_path.unlink()
        print(f"File {file_path} has been deleted.")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except PermissionError:
        print(f"You do not have permission to delete the file {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def process_args() -> tuple[str,str]:
    # Create the parser
    parser = argparse.ArgumentParser(description="Process a filename and event ID.")
    
    # Add positional arguments (no -- required)
    parser.add_argument("filename", type=str, help="The name of the file")
    parser.add_argument("event_id", type=str, help="The event ID")

    # Parse the arguments
    args = parser.parse_args()
    
    return (args.filename,args.event_id)
    

if __name__ == "__main__":
    from cal_parser.parser import parse_json_name, is_cal_file, get_path_from_filename
    from mongoDB.configure import connect_to_mongoDB

    BASE_DIR = Path("../../../temp_data/")
    TEST_PATH_TO_JSON = "../../../temp_data/test_google_.json"

    filename, event_id = process_args()

    CLIENT: MongoClient = connect_to_mongoDB()
    

    ### GET EVENT INFO From MONGO ###
    # event_dict = get_db_event_document(CLIENT,event_id)
    # invite_info: dict = get_preferred_dates_and_times(event_dict)
    # pref_dates: list[datetime] = invite_info["dates"]
    # invite_start: time = invite_info["start_time"]
    # invite_end: time = invite_info["end_time"]

    if parse_json_name(filename) == "upload" and is_cal_file(filename):
        PATH_TO_FILE: Path = get_path_from_filename(BASE_DIR,filename)
        ### pull in the file
        ### process the file
        #user_time_dict: dict = parse_ical_file(PATH_TO_FILE)
        print(PATH_TO_FILE)



        ### put all free times under the user
        ### get the free times for the entire event 
        ### update the event in mongo

        

    