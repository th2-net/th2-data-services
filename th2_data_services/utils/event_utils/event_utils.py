#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json

from th2_data_services.utils._types import Th2Event
import th2_data_services.utils.time
from typing import Callable, Dict, Iterable, Optional
from datetime import datetime

from th2_data_services.config import options

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
from th2_data_services.utils._is_sorted_result import IsSortedResult


# NOT STREAMING
# TODO - Can we have single function for events and messages?
#
# Will return list! Perhaps it's better to return Data?
def get_some(
    events: Iterable[Th2Event],
    event_type: Optional[str],
    max_count: int,  # TODO -- Slava - I think we need to add Optional = None, for unlimited.
    start: int = 0,
    failed: bool = False,  # ??
) -> Iterable[Th2Event]:
    """Returns limited list of events of specific eventType.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        event_type (str): Event Type To Extract
        max_count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    Returns:
        Iterable[Th2Event]

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
    counter = 0
    limit = start + max_count

    for event in events:
        if event_type is None or options.EVENT_FIELDS_RESOLVER.get_type(event) == event_type:
            if failed and options.EVENT_FIELDS_RESOLVER.get_status(event):
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


# NOT STREAMING
# TODO: Change name
def build_roots_cache(events: Iterable[Th2Event], depth: int, max_level: int) -> Dict:
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
        result[options.EVENT_FIELDS_RESOLVER.get_id(prev_level)] = {
            "eventName": options.EVENT_FIELDS_RESOLVER.get_name(prev_level),
            "eventPath": options.EVENT_FIELDS_RESOLVER.get_name(prev_level),
        }
    while level < depth:
        next_levels = get_children_from_parents_as_list(events, prev_levels, max_level)
        next_levels_count = len(next_levels)
        if next_levels_count == 0:
            break
        level += 1
        print(f"Level {level}: {next_levels_count} events")
        for next_level in next_levels:
            event_id = options.EVENT_FIELDS_RESOLVER.get_id(next_level)
            parent_id = options.EVENT_FIELDS_RESOLVER.get_parent_id(next_level)
            result[event_id] = {
                "eventName": options.EVENT_FIELDS_RESOLVER.get_name(next_level),
                "eventPath": result[parent_id]["eventPath"]
                + "/"
                + options.EVENT_FIELDS_RESOLVER.get_name(next_level),
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
    return th2_data_services.utils.time.extract_timestamp(
        options.EVENT_FIELDS_RESOLVER.get_start_timestamp(event)
    )


# NOT STREAMING
def extract_parent_as_json(
    events: Iterable[Th2Event],
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

    sub_events = sublist(
        events, datetime.fromisoformat(interval_start), datetime.fromisoformat(interval_end)
    )
    print(f"Sublist length = {len(sub_events)}")
    tree = get_event_tree_from_parent_id(
        sub_events, parent_id, 10, 10000, body_to_simple_processors
    )
    if not tree:
        return
    types_set = set(
        (type_[: type_.index(" [")] for type_ in tree["info"]["stats"] if type_ != "TOTAL")
    )
    tree["info"]["types_list"] = list(types_set)

    with open(json_file_path, "w") as file:
        json.dump(tree, file, indent=3)


def is_sorted(events: Iterable[Th2Event]) -> IsSortedResult:
    """Checks whether events are sorted.

    Args:
        events (Dict): Th2-Events

    Returns:
        IsSortedResult: Whether events are sorted and additional info (e.g. index of the first unsorted element).
    """
    is_sorted_result = IsSortedResult()
    flag = True
    previous_timestamp = None
    i = 0
    for event in events:
        if flag:
            previous_timestamp = options.EVENT_FIELDS_RESOLVER.get_start_timestamp(event)
            flag = False
        current_timestamp = options.EVENT_FIELDS_RESOLVER.get_start_timestamp(event)
        if previous_timestamp["epochSecond"] > current_timestamp["epochSecond"] or (
            previous_timestamp["epochSecond"] == current_timestamp["epochSecond"]
            and previous_timestamp["nano"] > current_timestamp["nano"]
        ):
            is_sorted_result.status = False
            is_sorted_result.first_unsorted = i
            break
        previous_timestamp = current_timestamp
        i += 1

    return is_sorted_result
