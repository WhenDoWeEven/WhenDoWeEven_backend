from typing import Any, Optional
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
from pathlib import Path
from bson import ObjectId


sys.path.append(str(Path(__file__).resolve().parent.parent))
from mongoDB.configure import connect_to_mongoDB

DATABASE = "BRICKHACK11"

### Collections ###
EVENTS_COLLECTION = "events"
USER_COLLECTIION = "users"


def add_test_free_times_to_user(client: MongoClient, user_id: str , field_value: str):
    # new_field = "free_times"
    # new_field_value = field_value

    # client[DATABASE][USER_COLLECTIION].update_one(
    #     {"_id": ObjectId(user_id)},  # Filter to match the specific document
    #     {"$set": {new_field: new_field_value}}  # Add the new field with the desired value
    # )

    # Ensure user_id is valid ObjectId
    user_oid = ObjectId(user_id)
    
    # Format the free_times field with pairs of start and end times
    free_times = []
    # print(field_value)
    # start = field_value[0]
    # end = field_value[1]
    free_times.append(field_value)
    # for start_time, end_time in field_value:
    #     free_times.append([start_time, end_time])  # Create pairs of [start, end]
    #    # Iterate over each pair of start and end times
    
    #Update the user's free_times field with the formatted pairs
    client[DATABASE][USER_COLLECTIION].update_one(
        {"_id": user_oid},  # Filter to match the specific document
        {"$set": {"free_times": free_times}}  # Add the new field with the list of pairs
    )
def add_test_event_id_to_user(client: MongoClient,event_id:str,user_id:str):
    # Ensure user_id is valid ObjectId
    user_oid = ObjectId(user_id)
    client[DATABASE][USER_COLLECTIION].update_one(
        {"_id": user_oid},  # Filter to match the specific document
        {"$set": {"eventId": event_id}}  # Add the new field with the list of pairs
    )

def add_test_preferred_dates(client: MongoClient, test_event_id: str, date: str) -> None:
    client[DATABASE][EVENTS_COLLECTION].update_one(
        {"eventId": test_event_id},  # Filter to match the specific document
        {"$push": {"preferedDates": date}}  # Add the new field with the list of pairs
    )

def add_user_free_time(client: MongoClient, user_id: str) -> None:
    pass
def update_user_free_time(client: MongoClient, user_id:str):
    pass
def add_group_event_free_time(client:MongoClient, event_id:str):
    pass
def update_group_event_free_time(client: MongoClient, event_id: str):
    pass

if __name__ == "__main__":
    client: MongoClient = connect_to_mongoDB()
    test_event_id: str =  "449195fd-4a05-46c0-9aa0-3cb5a4c9f4ef"
    test_user_ids: list[str] = ["67ba8fbdcb8cdd000fd26a28","67ba45a041da73b6d81044e7","67ba456440a2264064b359b8","67ba44e46354dd7b14a6fa5b","67ba44a804c9619c2c0fda51","67ba448e6ee18d03ddc3b8a6"]
    test_user_timestamps: list[str] = [["2024-01-01T00:00:00.000+00:00","2024-03-01T00:00:00.000+00:00"],
                                        ["2024-04-30T00:00:00.000+00:00","2024-06-29T00:00:00.000+00:00"],
                                        ["2024-08-28T00:00:00.000+00:00","2024-10-27T00:00:00.000+00:00"],
                                        ["2024-01-15T12:34:56.000+00:00","2024-03-18T09:47:12.000+00:00"],
                                        ["2024-05-05T14:23:39.000+00:00","2024-07-12T20:55:01.000+00:00"],
                                        ["2024-09-09T08:11:44.000+00:00","2024-11-02T16:03:18.000+00:00"]]
    pref_dates: list[str] = ["11/04/2024",
                            "01/12/2024",
                            "01/06/2024",
                            "07/04/2024"]
    # for user_id, user_timestamp in zip(test_user_ids,test_user_timestamps):
    #     add_test_free_times_to_user(client,user_id,field_value=user_timestamp)

    # for user_id in test_user_ids:
    #     add_test_event_id_to_user(client,test_event_id,user_id)

    for date in pref_dates:
        add_test_preferred_dates(client,test_event_id, date)

    # update_user_free_time()
    # update_group_free_time()

    client.close()