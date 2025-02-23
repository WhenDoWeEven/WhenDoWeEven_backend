import icalendar
from icalendar import Calendar
import json

from pymongo import MongoClient

def get_

def get_preferred_dates_and_times(client: MongoClient, event_id:str) -> dict

    ### Convert dates into datetime objects with the UTC timezone
    ###
    

    return {
        "dates":,
        "start_time":,
        "end_time",
    }

if __name__ == "__main__":
    get_user_json_calendar()
    convert_dict_cal_to_ics()