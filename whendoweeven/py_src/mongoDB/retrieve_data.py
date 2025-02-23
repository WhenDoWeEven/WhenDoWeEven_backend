import icalendar
from icalendar import Calendar
import json
from datetime import datetime, time
from pymongo import MongoClient
from bson import ObjectId
from collections import defaultdict

from whendoweeven.py_src.cal_parser.convert import convert_str_to_datetime_object, convert_timestamp_to_time_object, convert_timestamp_to_datetime_object
from mongoDB.configure import connect_to_mongoDB

DATABASE = "BRICKHACK11"

### Collections ###
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

def get_users_free_time_for_event(client: MongoClient, event_id:str) -> defaultdict[ObjectId, list[tuple[datetime,datetime]]]:
    """
    This function will get users free time dbased on the event that they're apart of. 

    Args:
        client (MongoClient): _description_
        event_id (str): _description_

    Returns:
        dict[list[tuple[datetime,datetime]]]: Every key will be an Object id. The value is a list of the times that the user is free
    """
    users_free_time = defaultdict(list)

    matching_users = client[DATABASE][USER_COLLECTIION].find({"evenId":event_id})
    
    user_oid: ObjectId
    free_times: list[tuple[datetime,datetime]] = []
    
    for user in matching_users:
        user_oid = ObjectId(user["_id"])

        # Prepare the list of free times for each user
        
        for free_time in user["free_times"]:
            start_time_str, end_time_str = free_time 
            
            start = convert_timestamp_to_datetime_object(start_time_str)
            end = convert_timestamp_to_datetime_object(end_time_str)

        
            free_times.append((start, end))

        # Assign the free times to the user (by ObjectId)
        users_free_time[user_oid] = free_times
        
    return users_free_time

def get_preferred_dates_and_times(event_dict: dict) -> dict:

    pref_dates: list[str] = event_dict["preferedDates"]
    pref_datetime_objects: list[datetime] = []

    ### These have to be time objects because a meeting on a various day can only happen between these times
    ### I have to re-write the other functions where I assumed that start and end were datetime objects
    start_time: time = convert_timestamp_to_time_object(event_dict["startTime"])
    end_time: time = convert_timestamp_to_time_object(event_dict["endTime"])
    
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

    client: MongoClient = connect_to_mongoDB()

    test_event_id: str = "449195fd-4a05-46c0-9aa0-3cb5a4c9f4ef"
    
    event_dict = get_db_event_document(client,event_id=test_event_id)
    print(event_dict)
    # get_db_user_document()
    # get_users_free_time_for_event()
    # get_preferred_dates_and_times()
