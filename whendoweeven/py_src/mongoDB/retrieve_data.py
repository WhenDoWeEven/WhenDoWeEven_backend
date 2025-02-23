from datetime import datetime, time
from pymongo import MongoClient
from bson import ObjectId
from collections import defaultdict

from mongoDB.configure import connect_to_mongoDB
from cal_parser.parser import convert_datetime_to_time,convert_str_to_datetime_object, convert_timestamp_to_datetime_object

DATABASE = "BRICKHACK11"

### Collections ###
EVENTS_COLLECTION = "events"
USER_COLLECTIION = "users"

def get_db_event_document(client: MongoClient, event_id:str) -> dict:
    event_document: dict = client[DATABASE][EVENTS_COLLECTION].find_one({"eventId":event_id})

    ### Close connection ###
    

    return event_document

def get_db_user_document(client: MongoClient, user_id: str) -> dict:
    user_oid: ObjectId = ObjectId(user_id)
    user_document: dict = client[DATABASE][USER_COLLECTIION].find_one({"_id":user_oid})

    ### Close connection ###
    #client.close()
    
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

    matching_users = client[DATABASE][USER_COLLECTIION].find({"eventId": event_id})
    
    user_oid: ObjectId
    
    
    for user in matching_users:
        user_oid = str(ObjectId(user["_id"]))
        free_times: list[tuple[datetime,datetime]] = []
        
        if "free_times" in user:
            for free_time in user["free_times"]:
                # Each free_time is expected to be a pair of timestamps
                if len(free_time) == 2:
                    start_time_str = free_time[0]
                    end_time_str = free_time[1]

                    # Convert timestamp strings to datetime objects
                    start = convert_timestamp_to_datetime_object(start_time_str)
                    end = convert_timestamp_to_datetime_object(end_time_str)

                    free_times.append((start, end))

        # Assign the user's free times to the dictionary (keyed by their ObjectId)
        users_free_time[user_oid] = free_times
        
    return users_free_time
def get_event_free_times(client: MongoClient, event_id:str) -> defaultdict[ObjectId, list[tuple[datetime,datetime]]]:
    users_free_time = defaultdict(list)

    matching_users = client[DATABASE][USER_COLLECTIION].find({"eventId": event_id})
    
    user_oid: ObjectId
    
    
    for user in matching_users:
        user_oid = str(ObjectId(user["_id"]))
        free_times: list[tuple[datetime,datetime]] = []
        
        if "free_times" in user:
            for free_time in user["free_times"]:
                # Each free_time is expected to be a pair of timestamps
                if len(free_time) == 2:
                    start_time_str = free_time[0]
                    end_time_str = free_time[1]

                    # Convert timestamp strings to datetime objects
                    start = convert_timestamp_to_datetime_object(start_time_str)
                    end = convert_timestamp_to_datetime_object(end_time_str)

                    free_times.append((start, end))

        # Assign the user's free times to the dictionary (keyed by their ObjectId)
        users_free_time[user_oid] = free_times
        
    return users_free_time
def get_preferred_dates_and_times(event_dict: dict) -> dict:
    pref_dates: list[str] = event_dict["preferedDates"]
    pref_datetime_objects: list[datetime] = []

    ### These have to be time objects because a meeting on a various day can only happen between these times
    # print(type(event_dict["startTime"]))
    # print(type(event_dict["startTime"]))
    start_time: time = convert_datetime_to_time(event_dict["startTime"])
    end_time: time = convert_datetime_to_time(event_dict["endTime"])
    
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
    test_user_ids: list[str] = ["67ba8fbdcb8cdd000fd26a28","67ba45a041da73b6d81044e7","67ba456440a2264064b359b8","67ba44e46354dd7b14a6fa5b","67ba44a804c9619c2c0fda51","67ba448e6ee18d03ddc3b8a6"]
    
    
    # event_dict = get_db_event_document(client,event_id=test_event_id)
    # print("EVENT DICT")
    # print(event_dict)
    # user_dict = get_db_user_document(client,test_user_ids[0])
    # print("USER DICT")
    # print(user_dict)

    
    # users_free_time = get_users_free_time_for_event(client,event_id=test_event_id)
    # print(users_free_time)
    test_event_dict = get_db_event_document(client,test_event_id)
    print(test_event_dict)
    print()
    print()
    print()
    print()
    pref_dates_and_times = get_preferred_dates_and_times(event_dict=test_event_dict)
    print(pref_dates_and_times)

    client.close()
