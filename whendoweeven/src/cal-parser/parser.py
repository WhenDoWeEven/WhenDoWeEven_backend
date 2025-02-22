import icalendar
from typing import Optional, Any
import json

import logging
import icalendar
from icalendar import Calendar
from icalevents import icalevents
from datetime import datetime, timezone
from pytz import UTC

"""
Calendar file parser based off of RFC 
    
"""

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

def get_events_in_range(parsed_data:dict ,start:datetime ,end:datetime) -> dict[str,list[dict]]:
    user_free_time: list[tuple] = []
    
    for event in parsed_data["events"]:
        
        sched_event_start: datetime = event["start"]
        sched_event_end: datetime = event["end"]


        user_free_start: datetime
        user_free_end: datetime
        if event_start < start and event_end < start:
            '''
            If the users event starts and ends before the start and end time of the range their being invited to...
            This event doesn't conflict with the range at all
            '''
            user_free_start = start
            user_free_end = end
        elif event_start > start and event_start < end:
            

    for busy_time in parsed_data["busy_times"]:
        busy_start: datetime = busy_time["start"]
        busy_end: datetime = busy_time["start"]

def main():

    file = "test_cal_files/test.ics"
    data = parse_ical_file(file)
    print(data["events"])

if __name__ == "__main__":
    main()