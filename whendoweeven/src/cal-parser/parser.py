import icalendar
from typing import Optional, Any
import json
import requests
import logging
import icalendar
from icalendar import Calendar
from icalevents import icalevents
from datetime import datetime, timezone, timedelta, date
import pytz
from pytz import UTC

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

                start_time = ensure_datetime(component.get('dtstart').dt)
                end_time = ensure_datetime(component.get('dtend').dt)

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
                start_time = ensure_datetime(component.get('dtstart').dt)
                end_time = ensure_datetime(component.get('dtend').dt)

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
    

def parse_ical_file(file_path: str) -> dict[str,list]:
    """
    Parses an .ics (iCalendar) file and extracts the events (VEVENT) and busy times (VFREEBUSY).
    
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

            start_time = ensure_datetime(component.get('dtstart').dt)
            end_time = ensure_datetime(component.get('dtend').dt)

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
            start_time = ensure_datetime(component.get('dtstart').dt)
            end_time = ensure_datetime(component.get('dtend').dt)

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

# Helper function to convert to datetime if it's a date object
def ensure_datetime(obj):
    if isinstance(obj, date) and not isinstance(obj,datetime):
        return datetime.combine(obj, datetime.min.time())
    return obj

# Convert all datetimes to UTC
def convert_to_utc(dt):
    # Check if datetime is naive (doesn't have timezone info)
    if dt.tzinfo is None:
        # If it's naive, localize it to UTC
        tz = pytz.utc
        dt = tz.localize(dt)  # Make it aware in UTC
    else:
        # If it's aware, convert to UTC
        dt = dt.astimezone(pytz.utc)
    return dt


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

def find_free_times(filtered_user_events:dict ,invite_range_start:datetime ,invite_range_end:datetime)-> list[datetime]:
    """
    These events have already been determined to be within the range of the invite event because they've gone through filter_out_events_outside_range

    Args:
        filtered_user_events (dict): _description_
        invite_range_start (datetime): _description_
        invite_range_end (datetime): _description_

    Returns:
        list[datetime]: _description_
    """
    index: int = 0
    free_times: list[tuple[datetime,datetime]] = []
    length: int = len(filtered_user_events["events"])

    while index < length:
        first_event_start: datetime = filtered_user_events["events"]["start"][index]
        first_event_end: datetime = filtered_user_events["events"]["end"][index]

        second_event_start: datetime = filtered_user_events["events"]["start"][index+1]
        second_event_end: datetime = filtered_user_events["events"]["end"][index+1]
        
        if first_event_end <= second_event_start:
            new_free_time_start = datetime(
                first_event_end.year,
                first_event_end.month,
                first_event_end.day,  # You missed `day` in your code
                first_event_end.hour,
                first_event_end.minute,
                tzinfo=first_event_end.tzinfo  # Carry over the timezone
            )
            new_free_time_end = datetime(
                second_event_start.year,
                second_event_start.month,
                second_event_start.day,
                second_event_start.hour,
                second_event_start.minute,
                tzinfo=second_event_start.tzinfo
            )

            free_times.append((new_free_time_start,new_free_time_end))
            
        first_event_start = second_event_start
        first_event_end = second_event_end

        ### increment the index first, then get the next event
        index+=1
        second_event_start = filtered_user_events["events"]["start"][index + 1]
        second_event_end = filtered_user_events["events"]["end"][index + 1]

        
    
    index = 0
    length_2: int = len(filtered_user_events["busy_times"])
    while index < length_2:
        first_event_start: datetime = filtered_user_events["busy_times"]["start"][index]
        first_event_end: datetime = filtered_user_events["busy_times"]["end"][index]

        second_event_start: datetime = filtered_user_events["busy_times"]["start"][index+1]
        second_event_end: datetime = filtered_user_events["busy_times"]["end"][index+1]
        
        if first_event_end <= second_event_start:
            new_free_time_start = datetime(
                first_event_end.year,
                first_event_end.month,
                first_event_end.day,  # You missed `day` in your code
                first_event_end.hour,
                first_event_end.minute,
                tzinfo=first_event_end.tzinfo  # Carry over the timezone
            )
            new_free_time_end = datetime(
                second_event_start.year,
                second_event_start.month,
                second_event_start.day,
                second_event_start.hour,
                second_event_start.minute,
                tzinfo=second_event_start.tzinfo
            )

            free_times.append((new_free_time_start,new_free_time_end))
            
        first_event_start = second_event_start
        first_event_end = second_event_end

        ### increment the index first, then get the next event
        index+=1
        second_event_start = filtered_user_events["busy_times"]["start"][index + 1]
        second_event_end = filtered_user_events["busy_times"]["end"][index + 1]
        index+=1

    return free_times

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


def main():
    file = "test_cal_files/test.ics"

    with open("test_cal_files/test_url.txt") as url_file:
        url_content = url_file.read()
       


    range_start: datetime = datetime(2024,10,1,14,30,0)
    range_end: datetime = datetime(2024,10,20,14,30,0)
    tz = timezone(timedelta(hours=3))  # UTC+3

    ### Make sure that ALL DATES are in UTC
    range_start_with_timezone = range_start.replace(tzinfo=tz)
    range_end_with_timezone = range_end.replace(tzinfo=tz)
    
    user_cal_url: dict = parse_ical_url(url_content)
    print(user_cal_url)
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    print("_______________________________________________________________")
    user_cal_url_filtered = filter_out_events_outside_range(user_events=user_cal_url,invite_range_start=range_start_with_timezone,invite_range_end=range_end_with_timezone)
    print(user_cal_url_filtered)
    # user_cal: dict = parse_ical_file(file)
    # print(user_cal)
    # print("_______________________________________________________________")
    # print("_______________________________________________________________")
    # print("_______________________________________________________________")
    # print("_______________________________________________________________")
    # user_cal_filtered = filter_out_events_outside_range(user_events=user_cal,invite_range_start=range_start_with_timezone,invite_range_end=range_end_with_timezone)
    # print(user_cal_filtered)
    

if __name__ == "__main__":
    main()