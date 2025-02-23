import json
import icalendar
from cal_parser import parser, convert
from mongoDB import upload_data
from pathlib import Path
import argparse

from whendoweeven.py_src.rec_algo.find_times_algo import find_free_times
from cal_parser.parser import is_cal_file,is_url


def get_user_json_calendar(user_json_cal: json) -> ics:
    # user_dict_cal = convert.convert_user_json_calendar_to_dict(user_json_cal)
    user_ics_cal = convert.convert_user_dict_calendar_to_ics(user_json_cal)


def get_user_google_calendar(user_google_cal:json) -> ics:
    
    # user_dict_cal = convert.convert_user_json_calendar_to_dict(user_google_cal)
    user_ics_cal = convert.convert_user_json_calendar_to_ics(user_google_cal)

def get_user_apple_calendar(user_apple_cal:json) -> ics:
    # user_dict_cal = convert.convert_user_json_calendar_to_dict(user_apple_cal)
    user_ics_cal = convert.convert_user_json_calendar_to_ics()

def parse_json_name(json_name:str) -> str:
    words_to_check = ["google", "apple", "microsoft", "upload", "url"]

    for word in words_to_check:
        if word.lower() in json_name.lower():
            return word

    return "No match found"

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

    
    PATH_TO_JSON = ""
    TEST_PATH_TO_JSON = "../../../temp_data/test_google_.json"

    filename: str
    event_id: str

    filename, event_id = process_args()
    if parse_json_name(filename) == "upload" and is_cal_file(filename):
        pass

    get_preferred_dates_and_times()