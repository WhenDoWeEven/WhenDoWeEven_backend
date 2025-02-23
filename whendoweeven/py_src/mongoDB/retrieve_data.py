import icalendar
from icalendar import Calendar
import json
from datetime import datetime, _Time
from pymongo import MongoClient
from bson import ObjectId
from collections import defaultdict

from cal_parser.convert import convert_str_to_datetime_object, convert_timestamp_to_time_object


DATABASE = "BRICKHACK11"
EVENTS_COLLECTION = "events"
USER_COLLECTIION = "users"

def get_db_event_document(client: MongoClient, event_id:str) -> dict:
    event_document: dict = client[DATABASE][EVENTS_COLLECTION].find_one({"eventId":event_id})

    ### Close connection ###
    client.close()

    return event_document

def get_db_user_document(client: MongoClient, user_id: str) -> dict:
    user_oid: ObjectId = ObjectId(user_id)
    user_document: dict = client[DATABASE][USER_COLLECTIION].find_one({"_id",user_oid})

    ### Close connection ###
    client.close()
    
    return user_document

def get_users_free_time_for_event(client: MongoClient, event_id:str) -> defaultdict[ObjectId, list[tuple[datetime,datetime]]] :
    """
    This function will get users based on the event that they're apart of. 

    Args:
        client (MongoClient): _description_
        event_id (str): _description_

    Returns:
        dict[list[tuple[datetime,datetime]]]: Every key will be an Object id. The key is a list of the times that the user is free
    """
    user_free_time: defaultdict[ObjectId,list[tuple[datetime,datetime]]] = {

    }
    matching_users = client[DATABASE][USER_COLLECTIION].find({"evenId":event_id})
    
    user_oid: ObjectId

    for user in matching_users:
        user["free_time"]
    

def get_preferred_dates_and_times(event_dict: dict) -> dict:

    pref_dates: list[str] = event_dict["preferedDates"]
    pref_datetime_objects: list[datetime] = []

    ### These have to be time objects because a meeting on a various day can only happen between these times
    ### I have to re-write the other functions where I assumed that start and end were datetime objects
    start_time: _Time = convert_timestamp_to_time_object(event_dict["startTime"])
    end_time: _Time = convert_timestamp_to_time_object(event_dict["endTime"])
    
    for date in pref_dates:
        pref_datetime_objects.append(convert_str_to_datetime_object(date))

    pref_dict = {
        "dates": pref_datetime_objects,
        "start_time":start_time,
        "end_time":end_time,
        }

    return pref_dict

if __name__ == "__main__":
    ### Test the functions
    
    get_db_event_document()
    get_db_user
    get_preferred_dates_and_times()
