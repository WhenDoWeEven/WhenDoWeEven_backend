import icalendar
from icalendar import Calendar
import json
from datetime import datetime, time, date
import pytz

def convert_user_json_calendar_to_ics() -> dict:
    pass

def convert_json_to_dict(json_file_path) -> dict:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data

# Convert all datetimes to UTC
def convert_datetime_to_utc(dt: datetime) -> datetime:
    # Check if datetime is naive (doesn't have timezone info)
    if dt.tzinfo is None:
        # If it's naive, localize it to UTC
        tz = pytz.utc
        dt = tz.localize(dt)  # Make it aware in UTC
    else:
        # If it's aware, convert to UTC
        dt = dt.astimezone(pytz.utc)
    return dt

def convert_datetime_to_time(dt: datetime) -> time:
    """
    Convert a datetime object to a time object.

    Args:
        dt (datetime): The datetime object to convert.

    Returns:
        time: The time portion of the datetime object.
    """
    if isinstance(dt, datetime):
        tz = pytz.utc
        dt = tz.localize(dt)
        return dt.time()  # Extract the time portion from the datetime
    else:
        raise ValueError("Expected a datetime object, got {0}".format(type(dt)))

def convert_timestamp_to_time_object(time_stamp:str) -> time:
    """
    Time stamp is in the form 2025-02-22T23:00:00.000+00:00

    Args:
        time_stamp (str): _description_

    Returns:
        time: _description_
    """
    #Convert to datetime object (parsing the ISO 8601 format)
    dt = datetime.fromisoformat(time_stamp.replace("Z", "+00:00"))

    # Convert to UTC (if not already)
    utc_dt = dt.astimezone(pytz.UTC)

    # Extract only the time (UTC)
    utc_time = utc_dt.time()

    return utc_time

def convert_timestamp_to_datetime_object(time_stamp:str) -> datetime:
    """
    Time stamp is in the form 2025-02-22T23:00:00.000+00:00

    Args:
        time_stamp (str): _description_

    Returns:
        datetime: _description_
    """

    if isinstance(time_stamp, str):
        if "Z" in time_stamp:  # Handle the "Z" for UTC
            time_stamp = time_stamp.replace("Z", "+00:00")
        dt= datetime.fromisoformat(time_stamp)
    else:
        raise ValueError(f"Invalid time_stamp format: {time_stamp}")
    

    # Convert to UTC (if not already)
    utc_dt = dt.astimezone(pytz.UTC)
    return utc_dt
def convert_str_to_datetime_object(date:str) -> datetime:
    """
    String is in the form month/day/year

    Args:
        date (str): _description_

    Returns:
        datetime: _description_
    """
    date_obj = datetime.strptime(date, "%m/%d/%Y")

    # Assign UTC timezone
    utc_timezone = pytz.utc
    date_obj_utc = utc_timezone.localize(date_obj)

    return date_obj_utc

# Helper function to convert to datetime if it's a date object
def convert_date_obj_to_datetime_obj(obj):
    if isinstance(obj, date) and not isinstance(obj,datetime):
        return datetime.combine(obj, datetime.min.time())
    return obj



if __name__ == "__main__":
    convert_user_json_calendar_to_ics()