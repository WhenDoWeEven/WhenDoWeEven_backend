import json
import sys
from pathlib import Path
import argparse
from datetime import datetime, time
from pymongo import MongoClient


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
    parser.add_argument("user_id",type=str, help="The user ID")
    # Parse the arguments
    args = parser.parse_args()
    
    return (args.filename,args.event_id, args.user_id)

def run_script(client: MongoClient, PATH_TO_FILE:str, event_id,user_id):
    ### Get the Event document ###
        event_document: dict = get_db_event_document(client,event_id)
        
        ### Get the preferred dates and times
        pref_dates_and_times = get_preferred_dates_and_times(event_dict=event_document)

        pref_dates: list[datetime] = pref_dates_and_times["dates"]
        start_time: time = pref_dates_and_times["start_time"]
        end_time: time = pref_dates_and_times["end_time"]

        ### tied to the user
        user_ical_dict: dict = parse_ical_file(PATH_TO_FILE)
        free_times = []
        for date in pref_dates:
            # Combine each date with the start and end times
            start_datetime = datetime.combine(date, start_time)
            end_datetime = datetime.combine(date, end_time)
            
            free_times.extend(find_free_times(filter_out_events_outside_range(user_events=user_ical_dict,invite_range_start=start_datetime, invite_range_end=end_datetime),start_datetime,end_datetime))

        
        ### put all free times under the user in mongo
        add_user_free_time(client,user_id,free_times)
            
        ### get the free times for the entire event 
        group_free_times = get_group_free_times()
        ## run the alogorithm 
        processed_algo_free_times = 
        ### update the group free times in mongoDB
        add_group_event_free_time(client,event_id,group_free_times=processed_algo_free_times)
        

if __name__ == "__main__":
    from cal_parser.parser import parse_json_name, is_cal_file, get_path_from_filename,parse_ical_file, filter_out_events_outside_range
    from mongoDB.configure import connect_to_mongoDB
    from mongoDB.upload_data import add_user_free_time,add_group_event_free_time
    from mongoDB.retrieve_data import get_db_event_document, get_preferred_dates_and_times
    from rec_algo.find_times_algo import find_free_times

    # BASE_DIR = Path("../temp_data")
    BASE_DIR = Path("/Users/jonathanbateman/Programming-Projects/WhenDoWeEven_backend/temp_data")
    # TEST_PATH_TO_JSON = "../../../temp_data/test_google_.json"

    filename, event_id, user_id = process_args()
    print(filename)
    print(event_id)
    print(user_id)
    CLIENT: MongoClient = connect_to_mongoDB()
    

    ### GET EVENT INFO From MONGO ###
    # event_dict = get_db_event_document(CLIENT,event_id)
    # invite_info: dict = get_preferred_dates_and_times(event_dict)
    # pref_dates: list[datetime] = invite_info["dates"]
    # invite_start: time = invite_info["start_time"]
    # invite_end: time = invite_info["end_time"]

    if parse_json_name(filename) == "upload" and is_cal_file(filename):
        ### pull in the file
        PATH_TO_FILE: Path = get_path_from_filename(BASE_DIR,filename)
        print("reached!")
        run_script(PATH_TO_FILE,event_id,user_id)
        
        
        # print(user_time_dict)

        ###
        
        

        

    