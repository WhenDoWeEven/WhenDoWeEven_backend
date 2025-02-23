import icalendar
from icalendar import Calendar
import json
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

DATABASE = "BRICKHACK11"
COLLECTION = "events"
def get_db_event(client: MongoClient, event_id:str) -> dict:
    event_oid: ObjectId = ObjectId(event_id)

    event_document = client[DATABASE][COLLECTION].find_one({"_id":event_id})

    ### Close connection ###
    client.close()

def get_db_user(client: MongoClient):


def get_preferred_dates_and_times(client: MongoClient, event_dict: dict) -> dict

    pref_dates: list[str] = event_dict["preferedDates"]
    pref_datetime_objects: list[]
    for dates in pref_dates:


    return {
        "dates":,
        "start_time":,
        "end_time",
    }

if __name__ == "__main__":
    