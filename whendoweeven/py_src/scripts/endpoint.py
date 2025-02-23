import json
import icalendar
from cal_parser import parser, convert
from mongoDB import upload_data

def get_user_json_calendar(user_json_cal: json) -> ics:
    # user_dict_cal = convert.convert_user_json_calendar_to_dict(user_json_cal)
    user_ics_cal = convert.convert_user_dict_calendar_to_ics(user_json_cal)


def get_user_google_calendar(user_google_cal) -> ics:
    
    # user_dict_cal = convert.convert_user_json_calendar_to_dict(user_google_cal)
    user_ics_cal = convert.convert_user_dict_calendar_to_ics()

def get_user_apple_calendar(user_apple_cal) -> ics:
    # user_dict_cal = convert.convert_user_json_calendar_to_dict(user_apple_cal)
    user_ics_cal = convert.convert_user_dict_calendar_to_ics()

def read_json(json:json) -> json:
    pass

def delete_temp_json_file()-> bool:
    pass


if __name__ == "__main__":

    PATH_TO_JSON = ""
    


    """
    User uploads
    User wants to read from URL
    google auth --> fetch calendar events info
    apple auth --> fetch calendar events info
    """