import json

import th2_data_services.utils.time
from typing import Callable, Dict, List, Optional
from datetime import datetime

# TODO -
#   1. events: List[Dict] -- should be Iterable[Th2Event], where Th2Event = Dict. It can be changed in the future
#   2. IDEA - it's difficult to understand what you will get when read some functions. I think add examples
#   3. I want to return special classes - not just dicts  because dicts
#       usually difficult to understand and customize

from th2_data_services.utils.event_utils.select import (
    get_roots,
    get_children_from_parents_as_list,
    sublist,
)


def get_some(
    events: List[Dict], event_type: Optional[str], count: int, start: int = 0, failed: bool = False
) -> List[Dict]:
    # NOT STREAMING
    # TODO - USEFUL ???
    #   What the example of this? look very rarely need to use
    # Will return list! Perhaps it's better to return Data?
    # TODO - move to select?
    """Returns limited list of events of specific eventType.

    Args:
        events (List[Dict]): TH2-Events
        event_type (str): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    Returns:
        List[Dict]

    Example:
        >>> get_some(events=events,
                     event_type="ModelCase",
                     count=100,
                     start=0
                     failed=False)
            [
                {**TH2-Event},
                ...
            ]

    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if event["eventType"] == event_type:
            if failed and event["successful"]:
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


# NOT STREAMING
# TODO: Change name
def build_roots_cache(events: List[Dict], depth: int, max_level: int) -> Dict:
    """Returns event path for each event.

    Notes:
        Event path from root to event, it's a string of event names separated by `/`

    Args:
        events: TH2-Events
        depth: Max depth to search
        max_level: Max events from leaf

    Returns:
        Dict[str, Dict[str, str]]

    Example:
        >>> build_roots_cache(events=events,
                              depth=10,
                              max_level=10)
            {
                eventId: {
                    eventName: "example event name",
                    eventPath: "rootName/.../currentEventName"
                },
                ...
            }
    """
    result = {}
    level = 1
    prev_levels = get_roots(events, max_level)
    print(f"Level {level}: {len(prev_levels)} events")
    for prev_level in prev_levels:
        result[prev_level["eventId"]] = {"eventName": prev_level["eventName"], "eventPath": prev_level["eventName"]}

    while level < depth:
        next_levels = get_children_from_parents_as_list(events, prev_levels, max_level)
        next_levels_count = len(next_levels)
        if next_levels_count == 0:
            break
        level += 1
        print(f"Level {level}: {next_levels_count} events")
        for next_level in next_levels:
            event_id = next_level["eventId"]
            parent_id = next_level["parentEventId"]
            result[event_id] = {
                "eventName": next_level["eventName"],
                "eventPath": result[parent_id]["eventPath"] + "/" + next_level["eventName"],
            }
        prev_levels = next_levels

    return result


# STREAMING
# TODO - perhaps we can move it to resolver.
def extract_start_timestamp(event: Dict) -> str:
    """Returns string representation of events timestamp.

    Args:
        event: TH2-Event

    Returns:
        str
    """
    return th2_data_services.utils.time.extract_timestamp(event["startTimestamp"])


# NOT STREAMING
def extract_parent_as_json(
    events: List[Dict],
    parent_id: str,
    json_file_path: str,
    interval_start: str,
    interval_end: str,
    body_to_simple_processors: Callable = None,
):
    """Parse parent into JSON format.

    Args:
        events (Dict): TH2-Events
        parent_id (str): Parent ID
        json_file_path (str): file JSON output path
        interval_start (str): Use events from this timestamp
        interval_end (str): Use events till this timestamp
        body_to_simple_processors (Callable, optional): Body categorizer function, defaults to None.

    Example:
        >>> extract_parent_as_json(
                events=data,
                parent_id="demo_parent_id",
                json_file_path="path/to/output.json",
                interval_start="2022-03-16T08:40:16",
                interval_end="2022-03-16T14:40:16"
            )

    JSON structure:
        {
            "info": {
                  "stats": EventType+Status (Frequency Table),
                  parent_event_details...
            }
            "child_id": {
                "info": { event_details...}
                "child_id": {
                    "info": { event_details...}
                    "body" { ... } # If event has body
                    "childId": { ... }
                }
            }
            "child_id2": { ... }
        }
    """
    from th2_data_services.utils.az_tree import get_event_tree_from_parent_id

    sub_events = sublist(events, datetime.fromisoformat(interval_start), datetime.fromisoformat(interval_end))
    print(f"Sublist length = {len(sub_events)}")
    tree = get_event_tree_from_parent_id(sub_events, parent_id, 10, 10000, body_to_simple_processors)
    if not tree:
        return
    types_set = set((type_[: type_.index(" [")] for type_ in tree["info"]["stats"] if type_ != "TOTAL"))
    tree["info"]["types_list"] = list(types_set)

    with open(json_file_path, "w") as file:
        json.dump(tree, file, indent=3)
