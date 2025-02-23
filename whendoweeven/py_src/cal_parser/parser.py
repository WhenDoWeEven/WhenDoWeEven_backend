import icalendar
from typing import Optional, Any
import json
import requests
import logging
import icalendar
from icalendar import Calendar
from datetime import datetime, timezone, timedelta, date
from pytz import UTC
from pathlib import Path
from convert import convert_to_utc, convert_date_obj_to_datetime_obj

from whendoweeven.py_src.rec_algo import find_times_algo as CREATE_RECS

"""
Calendar file parser based off of RFC 
    
"""

### TO-DO --> add a neurodivergent mode!
# Configure logging
logging.basicConfig(filename="parser-logs/debug_logs.log",level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def is_url(input_str: str) -> bool:
    """
    Check if user is passing in a url to a calendar or a downloaded file

    Args:
        input_str (str): _description_

    Returns:
        bool: True if the input is a url
    """
    return input_str.startswith(("http://", "https://"))

def parse_ical_url(url: str)-> dict[str,list]:
    """
    Fetches an .ics calendar from a URL and parses its events.

    :param url: The URL of the iCalendar (.ics) file.
    :return: List of event dictionaries containing summary, start, and end times.
    """
    parsed_data: dict[str,list] = {"events": [], 
                                   "busy_times": []}
    try:
        # Fetch the .ics file content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the calendar
        cal = icalendar.Calendar.from_ical(response.content)

    #     events = []
    #     for component in cal.walk():
    #         if component.name == "VEVENT":
    #             event = {
    #                 "summary": str(component.get('summary')),
    #                 "start": component.get('dtstart').dt,  # Can be datetime or date
    #                 "end": component.get('dtend').dt
    #             }
    #             events.append(event)

    #     return events
        # Iterate over the calendar components
        for component in cal.walk():
            # Check for VEVENT (Event)
            if component.name == "VEVENT":

                start_time = convert_date_obj_to_datetime_obj(component.get('dtstart').dt)
                end_time = convert_date_obj_to_datetime_obj(component.get('dtend').dt)

                # Convert start and end times to UTC
                start_time = convert_to_utc(start_time)
                end_time = convert_to_utc(end_time)

                if str(component.get('summary')) == 'Busy':
                    busy_time = {
                    "start": start_time,
                    "end": end_time,
                    "busy_type": str(component.get('freebusy'))  # can be 'busy' or 'free'
                    }
                    parsed_data["busy_times"].append(busy_time)
                else:
                    event = {
                        "summary": str(component.get('summary')),
                        "start": start_time,
                        "end": end_time
                    }
                    parsed_data["events"].append(event)
                
            # Check for VFREEBUSY (Busy Time)
            elif component.name == "VFREEBUSY":
                start_time = convert_date_obj_to_datetime_obj(component.get('dtstart').dt)
                end_time = convert_date_obj_to_datetime_obj(component.get('dtend').dt)

                # Convert start and end times to UTC
                start_time = convert_to_utc(start_time)
                end_time = convert_to_utc(end_time)

                busy_time = {
                    "start": start_time,
                    "end": end_time,
                    "busy_type": str(component.get('freebusy'))  # can be 'busy' or 'free'
                }
                parsed_data["busy_times"].append(busy_time)
        

        # Sort events and busy times by their start time
        parsed_data["events"].sort(key=lambda x: x["start"])  # Sort events by start time
        parsed_data["busy_times"].sort(key=lambda x: x["start"])  # Sort busy times by start time
        
            
        return parsed_data
    
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the .ics file: {e}")
        return []
    
def is_cal_file(filename) -> bool:
    extension = Path(filename).suffix  # Returns '.txt'

    if extension == ".ical" or extension == ".ics" or extension == ".ifb":
        return True
    else:
        return False
    
def parse_ical_file(file_path: str) -> dict[str,list]:
    """
    Parses an .ics (iCalendar) file and extracts the events (VEVENT) and busy times (VFREEBUSY).
    Sorts from earliest to latest
    
    :param file_path: Path to the .ics file.
    :return: Dictionary with events and busy times.
    """
    # Initialize a dictionary to hold events and busy times
    parsed_data: dict[str,list] = {"events": [], 
                                   "busy_times": []}
    
    # Open and read the .ics file
    with open(file_path, 'rb') as f:
        # Parse the content using the icalendar library
        cal = Calendar.from_ical(f.read())


    
    # Iterate over the calendar components
    for component in cal.walk():
        # Check for VEVENT (Event)
        if component.name == "VEVENT":

            start_time = convert_date_obj_to_datetime_obj(component.get('dtstart').dt)
            end_time = convert_date_obj_to_datetime_obj(component.get('dtend').dt)

            # Convert start and end times to UTC
            start_time = convert_to_utc(start_time)
            end_time = convert_to_utc(end_time)

            event = {
                "summary": str(component.get('summary')),
                "start": start_time,
                "end": end_time
            }
            parsed_data["events"].append(event)
        
        # Check for VFREEBUSY (Busy Time)
        elif component.name == "VFREEBUSY":
            start_time = convert_date_obj_to_datetime_obj(component.get('dtstart').dt)
            end_time = convert_date_obj_to_datetime_obj(component.get('dtend').dt)

            # Convert start and end times to UTC
            start_time = convert_to_utc(start_time)
            end_time = convert_to_utc(end_time)

            busy_time = {
                "start": start_time,
                "end": end_time,
                "busy_type": str(component.get('freebusy'))  # can be 'busy' or 'free'
            }
            parsed_data["busy_times"].append(busy_time)
    

    # Sort events and busy times by their start time
    parsed_data["events"].sort(key=lambda x: x["start"])  # Sort events by start time
    parsed_data["busy_times"].sort(key=lambda x: x["start"])  # Sort busy times by start time
    
    
    return parsed_data

def parse_json_name(json_name:str) -> str:
    words_to_check = ["google", "apple", "microsoft", "upload", "url"]

    for word in words_to_check:
        if word.lower() in json_name.lower():
            return word

    return "No match found"

def get_path_from_filename(base_dir: Path,filename:str) -> Path:
    # Create the new path by joining the base directory with the filename
    new_path = base_dir / filename

    # Check if the path exists
    if new_path.exists():
        print(f"Path exists: {new_path}")
    else:
        print(f"Path does not exist: {new_path}")
    
    return new_path

def filter_out_events_outside_range(user_events:dict ,invite_range_start:datetime ,invite_range_end:datetime) -> dict[str,list[dict]]:
    
    # Iterate backwards to prevent index shifting issues
    for index in reversed(range(len(user_events["events"]))):
        event = user_events["events"][index]
        sched_event_start: datetime = event["start"]
        sched_event_end: datetime = event["end"]

        if (not does_sched_event_overlap_with_invite(sched_event_start, sched_event_end, invite_range_start, invite_range_end) or 
            does_sched_event_completely_overlap_with_invite(sched_event_start, sched_event_end, invite_range_start, invite_range_end)):
            user_events["events"].pop(index)

     # Iterate backwards for busy times as well
    for index in reversed(range(len(user_events["busy_times"]))):
        busy_time = user_events["busy_times"][index]
        sched_event_start: datetime = busy_time["start"]
        sched_event_end: datetime = busy_time["end"]

        if (not does_sched_event_overlap_with_invite(sched_event_start, sched_event_end, invite_range_start, invite_range_end) or 
            does_sched_event_completely_overlap_with_invite(sched_event_start, sched_event_end, invite_range_start, invite_range_end)):
            user_events["busy_times"].pop(index)

    return user_events


def does_sched_event_overlap_with_invite(sched_event_start: datetime, sched_event_end: datetime, invite_range_start: datetime,invite_range_end: datetime)->bool:
    if sched_event_start > invite_range_start and sched_event_start < invite_range_end:
        ### If the start time of the event falls between the range return True
        return True
    elif sched_event_end > invite_range_start and sched_event_end < invite_range_end:
        ### If the end time of the event falls between the range
        return True
    elif sched_event_start < invite_range_start and sched_event_end > invite_range_end:
        return True
    return False

def does_sched_event_completely_overlap_with_invite(sched_event_start: datetime, sched_event_end: datetime, invite_range_start: datetime,invite_range_end: datetime)-> bool:
    if sched_event_start <= invite_range_start and sched_event_end >= invite_range_end:
        return True
    return False
    
    
if __name__ == "__main__":
    file = "test_cal_files/test.ics"

    with open("test_cal_files/test_url.txt") as url_file:
        url_content = url_file.read()
       


    range_start: datetime = datetime(2024,10,1,14,30,0)
    range_end: datetime = datetime(2024,10,20,14,30,0)
    tz = timezone(timedelta(hours=3))  # UTC+3

    ### Make sure that ALL DATES are in UTC
    range_start_with_timezone = range_start.replace(tzinfo=tz)
    range_end_with_timezone = range_end.replace(tzinfo=tz)
    
    # user_cal_url: dict = parse_ical_url(url_content)
    # print(user_cal_url)
    # print("_______________________________________________________________")
    # print("_______________________________________________________________")
    # print("_______________________________________________________________")
    # print("_______________________________________________________________")
    # user_cal_url_filtered = filter_out_events_outside_range(user_events=user_cal_url,invite_range_start=range_start_with_timezone,invite_range_end=range_end_with_timezone)
    # print(user_cal_url_filtered)
    user_cal: dict = parse_ical_file(file)
    print(user_cal)
    print("                      BASE USER CAL                            ")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    user_cal_filtered = filter_out_events_outside_range(user_events=user_cal,invite_range_start=range_start_with_timezone,invite_range_end=range_end_with_timezone)
    print("                   FILTERED ACCORDING TO INVITE                ")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print(user_cal_filtered)

    free_times: list[tuple[datetime,datetime]] = CREATE_RECS.find_free_times(filtered_user_events=user_cal_filtered,invite_range_start=range_start_with_timezone,invite_range_end=range_end_with_timezone)
    print("                         FREE TIMES                            ")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print(free_times)