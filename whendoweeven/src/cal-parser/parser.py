import icalendar
from typing import Optional, Any
import json

import logging
import icalendar
from icalendar import Calendar
from icalevents import icalevents
from datetime import datetime, timezone, timedelta
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

def parse_ical_file(file_path: str):
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
            event = {
                "summary": str(component.get('summary')),
                "start": component.get('dtstart').dt,
                "end": component.get('dtend').dt
            }
            parsed_data["events"].append(event)
        
        # Check for VFREEBUSY (Busy Time)
        elif component.name == "VFREEBUSY":
            busy_time = {
                "start": component.get('dtstart').dt,
                "end": component.get('dtend').dt,
                "busy_type": str(component.get('freebusy'))  # can be 'busy' or 'free'
            }
            parsed_data["busy_times"].append(busy_time)
    
    return parsed_data

def filter_out_events_outside_range(user_events:dict ,invite_range_start:datetime ,invite_range_end:datetime) -> dict[str,list[dict]]:
    
    index: int = 0
    for event in user_events["events"]:
        
        sched_event_start: datetime = event["start"]
        sched_event_end: datetime = event["end"]

        if does_sched_event_overlap_with_invite(sched_event_start,sched_event_end,invite_range_start,invite_range_end) == False:
            ### Remove that entry from the data
            del user_events["events"][index]
        index +=1

    ### reset the index
    index = 0
    for busy_time in user_events["busy_times"]:

        sched_event_start: datetime = busy_time["start"]
        sched_event_end: datetime = busy_time["end"]

        if does_sched_event_overlap_with_invite(sched_event_start,sched_event_end,invite_range_start,invite_range_end) == False:
            ### Remove that entry from the data
            del user_events["busy_times"][index]
        
        index += 1

    return user_events

def find_free_times()-> list[datetime]:
    pass

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
def does_sched_event_overlap_with_processed_events():
    pass
def main():

    file = "test_cal_files/test.ics"
    data = parse_ical_file(file)
    print(data["events"])

if __name__ == "__main__":
    main()