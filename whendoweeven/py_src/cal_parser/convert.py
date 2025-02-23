import icalendar
from icalendar import Calendar
import json
from datetime import datetime, _Time, date
import pytz

def convert_user_json_calendar_to_ics() -> dict:
    pass

def convert_json_to_dict(json_file_path) -> dict:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data

# Convert all datetimes to UTC
def convert_to_utc(dt:datetime) -> datetime:
    # Check if datetime is naive (doesn't have timezone info)
    if dt.tzinfo is None:
        # If it's naive, localize it to UTC
        tz = pytz.utc
        dt = tz.localize(dt)  # Make it aware in UTC
    else:
        # If it's aware, convert to UTC
        dt = dt.astimezone(pytz.utc)
    return dt
def convert_to_time_object(time_stamp:str) -> _Time:
    #Convert to datetime object (parsing the ISO 8601 format)
    dt = datetime.fromisoformat(time_stamp.replace("Z", "+00:00"))

    # Convert to UTC (if not already)
    utc_dt = dt.astimezone(pytz.UTC)

    # Extract only the time (UTC)
    utc_time = utc_dt.time()

    return utc_time

# Helper function to convert to datetime if it's a date object
def convert_date_obj_to_datetime_obj(obj):
    if isinstance(obj, date) and not isinstance(obj,datetime):
        return datetime.combine(obj, datetime.min.time())
    return obj

def convert_to_datetime_object(date:str) -> datetime:
    date_obj = datetime.strptime(date, "%m/%d/%Y")

    # Assign UTC timezone
    utc_timezone = pytz.utc
    date_obj_utc = utc_timezone.localize(date_obj)

    return date_obj_utc

if __name__ == "__main__":
    convert_user_json_calendar_to_ics()