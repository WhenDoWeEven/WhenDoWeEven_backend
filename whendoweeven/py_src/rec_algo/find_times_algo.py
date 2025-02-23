from datetime import datetime
import sys
from pathlib import Path


from cal_parser.parser import parse_ical_file


sys.path.append(str(Path(__file__).resolve().parent.parent))

def find_free_times(filtered_user_events: dict[str, list[dict[str, datetime]]], invite_range_start: datetime, invite_range_end: datetime) -> list[tuple[datetime, datetime]]:
    """
    Finds gaps (free times) between already filtered events within an invite range.

    Args:
        filtered_user_events (dict): Dictionary containing "events" and "busy_times".
        invite_range_start (datetime): The start of the invite range.
        invite_range_end (datetime): The end of the invite range.

    Returns:
        list[tuple[datetime, datetime]]: List of free time intervals as (start, end).
    """

    free_times: list[tuple[datetime, datetime]] = []

    # Merge events and busy times into a single sorted list
    all_events = sorted(
        filtered_user_events["events"] + filtered_user_events["busy_times"],
        key=lambda e: e["start"]
    )

    # Case: No events at all, the entire range is free
    if not all_events:
        return [(invite_range_start, invite_range_end)]

    # Check for free time before the first event
    first_event_start = all_events[0]["start"]
    if invite_range_start < first_event_start:
        free_times.append((invite_range_start, first_event_start))

    # Check for free times between events
    for i in range(len(all_events) - 1):
        first_event_end = all_events[i]["end"]
        second_event_start = all_events[i + 1]["start"]

        if first_event_end <= second_event_start:
            free_times.append((first_event_end, second_event_start))

    # Check for free time after the last event
    last_event_end = all_events[-1]["end"]
    if last_event_end < invite_range_end:
        free_times.append((last_event_end, invite_range_end))

    return free_times

def write_to_local_file():
    """
    Write the recommended times to a local cal file.
    """
    pass


if __name__ == "__main__":
    find_free_times()