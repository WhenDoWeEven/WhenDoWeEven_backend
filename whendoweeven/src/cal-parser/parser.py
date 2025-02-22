import icalendar
from typing import Optional, Any
import json

import logging
from icalendar import Calendar

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

import logging
from icalendar import Calendar

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_ical_content(file_path: str) -> dict:
    """
    Reads an iCalendar file (.ics, .ical, .ifb) and extracts both VEVENT (events) 
    and VFREEBUSY (free/busy) data if present.

    :param file_path: Path to the calendar file.
    :return: Dictionary containing "events" and "freebusy" data.
    """
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()

        cal = Calendar.from_ical(file_content)

        events = [comp.to_ical().decode("utf-8") for comp in cal.walk("VEVENT")]
        freebusy = [comp.to_ical().decode("utf-8") for comp in cal.walk("VFREEBUSY")]

        if not events and not freebusy:
            return {"error": "No VEVENT or VFREEBUSY data found."}

        return {"events": "\n".join(events), "freebusy": "\n".join(freebusy)}

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return {"error": "File not found."}
    except Exception as e:
        logging.error(f"An error occurred while processing {file_path}: {e}")
        return {"error": str(e)}

# Example usage:
ical_data = extract_ical_content("calendar.ics")
print("Events:\n", ical_data.get("events", "No event data"))
print("\nFree/Busy:\n", ical_data.get("freebusy", "No free/busy data"))


# Example usage:
ics_content = extract_ical_content("calendar.ics")
print(ics_content)

    pass
def parse_ics(ics_file:str):
    pass
def parse_ical(ical_file):
    pass
def parse_ifb(ifb_file):
    pass


def main():
    pass

if __name__ == "__main__":
    main()