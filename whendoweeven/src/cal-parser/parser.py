import icalendar
from typing import Optional, Any
import json

import logging
import icalendar
from icalendar import Event
from icalevents import icalevents
from datetime import datetime, timezone

"""
Calendar file parser based off of RFC 
    
"""

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def is_url(input_str: str) -> bool:
    """
    Check if user is passing in a url to a calendar or a downloaded file

    Args:
        input_str (str): _description_

    Returns:
        bool: True if the input is a url
    """
    return input_str.startswith(("http://", "https://"))
def extract_ical_content(cal_location: str, start: datetime, end: datetime) -> dict:
    """
    Reads an iCalendar file (.ics, .ical, .ifb) and extracts both VEVENT (events) 
    and VFREEBUSY (free/busy) data within a given time range.

    :param cal_location: Path to the calendar file.
    :param start: Start date (datetime object) for filtering events.
    :param end: End date (datetime object) for filtering events.
    :return: Dictionary containing "events" and "freebusy" data.
    """

    calendar_events: list[Event]
    try:

        if is_url(cal_location):
            calendar_events = icalevents.events(url=cal_location, start=start, end=end,fix_apple=True,tzinfo=timezone.utc)
        else:
            calendar_events = icalevents.events(file=cal_location, start=start, end=end, fix_apple=True,tzinfo=timezone.utc)
        
        event_data = []
        freebusy_data = []
        
        for e in calendar_events:
            # Distinguish between event types
            if e.name == "VEVENT":
                event_data.append(str(e))
            elif e.name == "VFREEBUSY":
                freebusy_data.append(str(e))

        if not event_data and not freebusy_data:
            logging.warning("No VEVENT or VFREEBUSY data found in the given time range.")
            return {"error": "No VEVENT or VFREEBUSY data found."}

        return {
            "events": "\n".join(event_data) if event_data else "No events found",
            "freebusy": "\n".join(freebusy_data) if freebusy_data else "No free/busy data found",
        }

    except FileNotFoundError:
        logging.error(f"File not found: {cal_location}")
        return {"error": "File not found."}
    except Exception as e:
        logging.error(f"An error occurred while processing {cal_location}: {e}")
        return {"error": str(e)}





def main():
    # Example usage:
    start_date = datetime(2025, 2, 22)
    end_date = datetime(2025, 3, 1)

    ical_data = extract_ical_content("test_cal_files/test.ics", start=start_date, end=end_date)
    print(ical_data)
    # # Example usage:
    # ical_data = extract_ical_content("calendar.ics")
    # print("Events:\n", ical_data.get("events", "No event data"))
    # print("\nFree/Busy:\n", ical_data.get("freebusy", "No free/busy data"))
    # extract_ical_content("")

if __name__ == "__main__":
    main()