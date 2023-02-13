from typing import Callable, Dict, List, Tuple, Set, Union, Optional
from datetime import datetime
from th2_data_services.utils import misc_utils
import json
from collections import defaultdict
from tabulate import tabulate

# TODO -
#   1. events: List[Dict] -- should be Iterable[Th2Event], where Th2Event = Dict. It can be changed in the future
#   2. IDEA - it's difficult to understand what you will get when read some functions. I think add examples
#   3. Rename all docstrings word Gets to Returns. That's different things.


def get_category_frequencies(
    events: List[Dict], categories: List[str], categorizer: Callable, aggregation_level: str = "seconds"
) -> List[List[str]]:
    """Gets Event Frequencies Based On Event Category.

    Args:
        events (List[Dict]): TH2-Events
        categories (List[str]): Event Categories
        categorizer (Callable): Categorizer Method
        aggregation_level (Optional, str): Aggregation Level

    Returns:
        List[List[str]]
    """
    return misc_utils.get_objects_frequencies(
        events,
        categories,
        categorizer,
        lambda e: e["startTimestamp"]["epochSecond"],
        aggregation_level=aggregation_level,
    )


# STREAMING
# TODO - slava
#   Do we really need it? Why user cannot just use this one line?
#   Maybe better to have prepared list of categorizers? e.g. in form of Adapters.
#   get_category_frequencies(events, types_list, EventCategorizer.type)
#   or idea to creat class TypeFrequences
#   GetFrequences.by_type_category
#   GetFrequences.by_name_category
#   GetFrequences.by_category
def get_type_frequencies(events: List[Dict], types_list: List[str], aggregation_level="seconds") -> List[List[str]]:
    """Returns Event Frequencies Based On EventType.

    Args:
        events (List[Dict]): TH2-Events
        types_list (List[str]): Event Types
        aggregation_level (Optional, str): Aggregation Level

    Returns:
        List[List[str]]: List Of Frequency Lists
    """
    return get_category_frequencies(events, types_list, lambda e: e["eventType"], aggregation_level)


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
# categorizer - expects that it will return str
# --
# example
# eu.get_category_totals(d2, lambda e: e["eventType"])
# defaultdict(<class 'int'>, {'Service event [ok]': 9531, 'Info [ok]': 469})
# eu.get_category_totals(d2, lambda e: 'aaa')
# defaultdict(<class 'int'>, {'aaa [ok]': 10000})
def get_category_totals(events: List[Dict], categorizer: Callable, ignore_status: bool = False) -> Dict[str, int]:
    """Gets Dictionary quantities of events for different categories.

    Args:
        events (List[Dict]): TH2-Events
        categorizer (Callable): Transformer function
        ignore_status (bool): Concatenate status string, defaults to False.

    Returns:
        Dict[str, int]
    """
    event_categories = defaultdict(int)
    for event in events:
        category = categorizer(event)
        if not ignore_status:
            status = " [ok]" if event["successful"] else " [fail]"
            category += status
        event_categories[category] += 1

    return event_categories


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
# example
# eu.get_attached_messages_totals(d1)
# defaultdict(<class 'int'>, {'envtn2_msfix5:first': 25262, 'envtn2_jpmfix1:second': 1702, 'env2_gscofixg2:second': 1702,...
def get_attached_messages_totals(events: List[Dict]) -> Dict[str, int]:
    """Returns Dictionary quantities of messages attached to events for each stream.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]
    """
    streams = defaultdict(int)
    for event in events:
        for message_id in event["attachedMessageIds"]:
            key = message_id[: message_id.rindex(":")]
            streams[key] += 1

    return streams


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
def get_attached_message_ids(events: List[Dict]) -> Set[str]:
    """Returns the set of unique message IDs linked to all events.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Set[str]
    """
    return set(message_id for event in events for message_id in event["attachedMessageIds"])


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["parentEventId, eventId"] should be updated by resolver
# TODO - It returns only parent events that not present in the events.
#   Perhaps we need to find better name
# we use something similar in our EventTree
def get_prior_parent_ids(events: List[Dict]) -> Set[str]:
    """Returns only parent events that not present in the events.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Set[str]
    """
    all_event_ids = set()
    parent_ids = set()
    for event in events:
        parent_id = event["parentEventId"]
        event_id = event["eventId"]
        if parent_id is not None and not parent_id in all_event_ids:
            parent_ids.add(parent_id)
        if event_id in parent_ids:
            parent_ids.remove(event_id)
        all_event_ids.add(event_id)

    return parent_ids


# USEFUL
# NOT STREAMING - keeps events
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
# BE AWARE!! - it can it all your memory
# O(N*M)
def get_attached_message_ids_index(events: List[Dict]) -> Dict[str, list]:
    """Gets dict of lists of related events by unique message IDs.

    Note:
        This object can occupy large amount of memory for big collections of events - use with caution
        Keeps in memory all events that are linked to messages.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, list]
    """
    result = defaultdict(list)
    for event in events:
        for message_id in event["attachedMessageIds"]:
            result[message_id].append(event)

    return result


# TODO - USEFULL ??? Do we need ignore status??
# partly the same as get_category_totals and WO ignore status
# Because it's the same we can you get_category_totals inside
#
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
def get_type_totals(events: List[Dict]) -> Dict[str, int]:
    """Gets dictionary quantities of events for different event types.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]
    """
    event_types = defaultdict(int)
    for event in events:
        status = " [ok]" if event["successful"] else " [fail] "
        event_type = event["eventType"] + status
        event_types[event_type] += 1

    return event_types


# NOT STREAMING
# TODO - USEFUL ???
#   What the example of this? look very rarely need to use
# Will return list! Perhaps it's better to return Data?
def get_some(
    events: List[Dict], event_type: Optional[str], count: int, start: int = 0, failed: bool = False
) -> List[Dict]:
    """Gets limited list of events of specific eventType.

    Args:
        events (List[Dict]): TH2-Events
        event_type (str): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    Returns:
        List[Dict]
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
def get_related_events(events: List[Dict], messages: List[Dict], count: int) -> List[Dict]:
    """Gets limited list of events of linked to any message within specified messages objects collection.

    Args:
        events: TH2-Events
        messages: TH2-Messages
        count: Maximum number of events to extract

    Returns:
        List[Dict]
    """
    result = []
    msg_ids = set(message["messageId"] for message in messages)

    for event in events:
        for msg_id in event["attachedMessageIds"]:
            if msg_id in msg_ids:
                result.append(event)
                if len(result) == count:
                    return result

    return result


# NOT STREAMING
# TODO - duplicates get_some (get_events)
def get_events_by_category(
    events: List[Dict], category: str, count: int, categorizer: Callable, start=0, failed=False
) -> List[Dict]:
    """Gets limited list of events of specific category produced by custom categorizer.

    Args:
        events (List[Dict]): TH2-Events
        category (str): Event category to extract
        count (int): Maximum number of events to extract
        categorizer (Callable): Transformer function
        start (int, optional): Start iteration index, defaults to 0.
        failed (bool, optional): Extract only failed events, defaults to False.

    Returns:
        List[Dict]
    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if categorizer(event) == category:
            if failed and event["successful"]:
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


# USEFUL
# NOT STREAMING
def get_roots(events: List[Dict], count: int, start: int = 0) -> List[Dict]:
    """Gets limited list of root events (events without parents).

    Args:
        events (List[Dict]): TH2-Events
        count (int): Maximum number of events to extract
        start (int, optional): Iteration Start Index, Defaults to 0.

    Returns:
        List[Dict]: List Of Root Events.
    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if event["parentEventId"] is None:
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


# USEFUL
# NOT STREAMING
def get_parents(events: List[Dict], children: List[Dict]):
    """Gets all parent events of linked to any event within specified events objects collection.

    Args:
        events (List[Dict]): TH2-Events
        children (List[Dict]): Extract Parents By Child Events

    """
    parent_ids = set(child["parentEventId"] for child in children)
    return [event for event in events if event["eventId"] in parent_ids]


# NOT STREAMING
def get_children_from_parent_id(events: List[Dict], parent_id: str, max_events: int) -> Tuple[List[Dict], Dict]:
    """Gets limited list of direct children events.

    Args:
        events (List[Dict]): TH2-Events
        parent_id (str): Parent ID
        max_events (int): Maximum number of events to extract

    Returns:
        Tuple[List[Dict], Dict]: Children Events, Parent Event
    """
    children = []
    resolved_parent = {}
    counter = 0
    for event in events:
        if event["eventId"] == parent_id:
            resolved_parent = event
        if event["parentEventId"] == parent_id:
            children.append(event)
            counter += 1
            if counter == max_events:
                break

    return children, resolved_parent


# NOT STREAMING
def get_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int) -> Tuple[Dict[str, list], int]:
    """Gets limited list of direct children events for each event in parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[str]): TH2-Events
        max_events (int): Maximum number of events to extract

    Returns:
        Tuple(Dict[str, list], int): Parent-Children, Events Count
    """
    parent_ids = set(parent["eventId"] for parent in parents)
    result = defaultdict(list)
    events_count = 0
    for event in events:
        parent_id = event["parentEventId"]
        if parent_id not in parent_ids:
            continue
        events_count += 1
        if len(result[parent_id]) <= max_events:
            result[parent_id].append(event)

    return result, events_count


# NOT STREAMING
def get_children_from_parents_as_list(events: List[Dict], parents: List[Dict], max_events: int) -> List[Dict]:
    """Gets limited list of direct children events for each event in parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): TH2-Events
        max_events(int): Maximum number of events to extract

    Returns:
        Dict[str, list]: Children Events
    """
    parent_ids = set(parent["eventId"] for parent in parents)
    result = []
    parents_counts = defaultdict(int)
    for event in events:
        parent_id = event["parentEventId"]
        if parent_id not in parent_ids:
            continue
        if parents_counts[parent_id] <= max_events:
            result.append(event)
        parents_counts[parent_id] += 1

    return result


# NOT STREAMING
def sublist(events: List[Dict], start_time: datetime, end_time: datetime) -> List[Dict]:
    """Filter Events Based On Timeframe.

    Args:
        events (List[Dict]): TH2-Events
        start_time (datetime): Start
        end_time (datetime): End Time

    Returns:
        List[Dict]: Filtered Events.
    """
    result = []
    start_time = datetime.timestamp(start_time)
    end_time = datetime.timestamp(end_time)
    for event in events:
        event_time = event["startTimestamp"]["epochSecond"]
        if start_time <= event_time <= end_time:
            result.append(event)

    return result


# NOT STREAMING
# TODO - not clear docstring
# TODO - hardcoded get_event_tree_from_parent_id parameters - is it Ok?
def extract_parent_as_json(
    events: Dict,
    parent_id: str,
    json_file_path: str,
    interval_start: str,
    interval_end: str,
    body_to_simple_processors: Callable = None,
):
    """Parse Parent Into JSON Format.

    Args:
        events (Dict): TH2-Events
        parent_id (str): Parent ID
        json_file_path (str): JSON Output Path
        interval_start (str): Interval Start
        interval_end (str): Interval End
        body_to_simple_processors (Callable, optional): Body Transformer Function. Defaults to None.
    """
    # TODO - temporary imported here to escape circular import
    from th2_data_services.utils.az_tree import get_event_tree_from_parent_id

    sub_events = sublist([events], datetime.fromisoformat(interval_start), datetime.fromisoformat(interval_end))
    print(f"Sublist Length = {len(sub_events)}")
    tree = get_event_tree_from_parent_id(sub_events, parent_id, 10, 10000, body_to_simple_processors)
    types_set = set((type_[: type_.index(" [")] for type_ in tree["info"]["stats"] if type_ != "TOTAL"))
    tree["info"]["types_list"] = list(types_set)

    with open(json_file_path, "w") as file:
        json.dump(tree, file, indent=3)


# NOT STREAMING
# TODO: Change name
def build_roots_cache(events: List[Dict], depth: int, max_level: int) -> Dict:
    """Returns event path for each event.

    | Event path from root to event, it's a string of event names separated by `/`
    |
    | result:
    | { eventId: { eventName: "example event name", eventPath: "rootName/.../currentEventName" }, ... }

    Args:
        events: TH2-Events
        depth: Max depth to search
        max_level: Max events from leaf

    Returns:
        Dict[str, Dict[str, str]]
    """
    result = {}
    level = 1
    prev_levels = get_roots(events, max_level)
    print("First level :", len(prev_levels))
    for prev_level in prev_levels:
        result[prev_level["eventId"]] = {"eventName": prev_level["eventName"], "eventPath": prev_level["eventName"]}
    while level < depth:
        next_levels = get_children_from_parents_as_list(events, prev_levels, max_level)
        print("Next level :", len(next_levels))
        for next_level in next_levels:
            event_id = next_level["eventId"]
            parent_id = next_level["parentEventId"]
            result[event_id] = {
                "eventName": next_level["eventName"],
                "eventPath": result[parent_id]["eventPath"] + "/" + next_level["eventName"],
            }
        prev_level = next_levels
        level += 1

    return result


# STREAMING
def extract_time(event) -> str:
    """Gets string representation of events timestamp.

    Args:
        event: TH2-Event

    Returns:
        str
    """
    return misc_utils.extract_timestamp(event["startTimestamp"])


# STREAMING
def print_attached_messages_totals(events: List[Dict], return_html: bool = False) -> Union[None, str]:
    """Prints Dictionary quantities of messages attached to events for each stream + direction.

    Args:
        events (List[Dict]): TH2-Events
        return_html (bool): Return HTML Format

    """
    data = get_attached_messages_totals(events)
    return misc_utils.print_stats_dict(data, return_html)


# STREAMING
def print_category_totals(
    events: List[Dict], categorizer: Callable, return_html: bool = False, ignore_status: bool = False
) -> Union[None, str]:
    """Prints Dictionary quantities of events for different categories.

    Args:
        events (List[Dict]): TH2-Events
        categorizer (Callable): Categorizer Method
        return_html (bool): Return HTML Format, defaults to False
        ignore_status (bool): Get status of events, defaults to False

    Returns:
        Union[None, str]
    """
    data = get_category_totals(events, categorizer, ignore_status=ignore_status)
    return misc_utils.print_stats_dict(data, return_html)


# STREAMING
def print_event(event: Dict) -> None:
    """Prints event in human-readable format.

    Args:
        event (List[Dict]): TH2-Events

    """
    print(
        f"{extract_time(event)} > [{'ok' if event['successful'] else 'fail'}] "
        f"Type: {event['eventType']} "
        f"Name: {event['eventName']} "
        f"ID: {event['eventId']} "
        f"Parent:{event['parentEventId']} "
        f"Body:{event['body']}"
    )


# NOT STREAMING
# PREV name print_some_raw
def print_events_raw(events: List[Dict], event_type: str, count: int, start: int = 0, failed: bool = False) -> None:
    """Prints limited list of events of specific eventType in dictionary format.

    Args:
        events (List[Dict]): TH2-Events
        event_type (set): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    """
    records = get_some(events, event_type, count, start, failed)
    for r in records:
        print(r)


# NOT STREAMING
def print_some(events: List[Dict], event_type: str, count: int, start: int = 0, failed: bool = False) -> None:
    """Prints limited list of events of specific eventType in human-readable format.

    Args:
        events (List[Dict]): TH2-Events
        event_type (set): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    """
    records = get_some(events, event_type, count, start, failed)
    for r in records:
        print_event(r)


# NOT STREAMING
def print_some_by_category(
    events: List[Dict], category: str, count: int, categorizer: Callable, start: int = 0, failed: bool = False
) -> None:
    """Print limited events by category.

    Args:
        events (List[Dict]): TH2-Events
        category (str): Event category to extract
        count (int): Maximum number of events to extract
        categorizer (Callable): Transformer function
        start (int, optional): Start iteration index, defaults to 0.
        failed (bool, optional): Extract only failed events, defaults to False.

    """
    records = get_events_by_category(events, category, count, categorizer, start, failed)
    for r in records:
        print_event(r)


# STREAMING
def print_roots(events: List[Dict], count: int, start: int = 0) -> None:
    """Prints limited list of root events (events without parents).

    Args:
        events (List[Dict]): TH2-Events
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.

    """
    records = get_roots(events, count, start)
    for r in records:
        print_event(r)


# STREAMING
def print_children(events: List[Dict], parent: str, count: int, verbose: bool = True):
    """Prints limited list of direct children events.

    Args:
        events (List[Dict]): TH2-Events
        parent (str): Parent ID
        count (int): Maximum number of events to extract
        verbose (bool): Verbose output, defaults to True.

    """
    records = get_children_from_parent_id(events, parent, count)
    fprint = print_event if verbose is True else print
    for r in records:
        fprint(r)


# STREAMING
def print_type_totals(events: List[Dict], return_html: bool = False) -> Union[None, str]:
    """Prints dictionary quantities of events for different event types.

    Args:
        events (List[Dict]): TH2-Events
        return_html (bool): HTML format, defaults to False

    Returns:
        Union[None, str]
    """
    event_types = get_type_totals(events)
    return misc_utils.print_stats_dict(event_types)


# STREAMING
def print_type_frequencies(
    events: List[Dict], event_types: List[str], aggregation_level: str = "seconds", return_html=False
) -> Union[None, str]:
    """Prints table of events per seconds or each second when there were events within events stream.

    Args:
        events: TH2-Events
        event_types: List of event types to analyze
        aggregation_level: Aggregation level
        return_html: Return HTML format, defaults to False

    """
    table = get_type_frequencies(events, event_types)
    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))


# STREAMING
def print_category_frequencies(
    events: List[Dict],
    event_types: List[str],
    categorizer: Callable,
    aggregation_level: str = "seconds",
    return_html: bool = False,
) -> Union[None, str]:
    """Prints table of events per seconds or each second when there were events within events stream.

    Args:
        events (List[Dict]): TH2-Events
        event_types (List[str]): Event Types To Extract
        categorizer (Callable): Transformer Function
        aggregation_level (str): Aggregation Level
        return_html: Return HTML Format

    Returns:
        Union[None, str]
    """
    data = get_category_frequencies(events, event_types, categorizer, aggregation_level)
    return misc_utils.print_stats_dict(data, return_html)


# NOT STREAMING
def print_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int = 10_000) -> None:
    """Prints limited list of direct children events for each event in parents_list.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): Parent TH2-Events
        max_events (int): Maximum number of events to extract, default to 10'000

    """
    tree, count = get_children_from_parents(events, parents, max_events)
    print(f"####### Retrieved Children: {count}")
    for parent in parents:
        print(parent)
        print(f">>>>>>> Children: {len(tree[parent['eventId']])}")
        for child in tree[parent["eventId"]]:
            print_event(child)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


# NOT STREAMING
def print_children_stats_from_parents(
    events: List[Dict], parents: List[Dict], max_events: int = 10_000, return_html: bool = False
) -> Union[None, str]:
    """Prints statistics with number of children and their duration for each event in parents_list.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): Parent TH2-Events
        max_events (int): Maximum number of events to extract, default to 10'000
        return_html (bool): Return HTML format, defaults to False

    """
    tree, _ = get_children_from_parents(events, parents, max_events)
    table = [["eventName", "status", "eventId", "child_pass", "child_fail", "start", "end"]]  # Header
    for parent in parents:
        start_timestamp, end_timestamp = 0, 0
        events_passed, events_failed = 0, 0
        for child in tree[parent["eventId"]]:
            child_start_time_epoch = child["startTimestamp"]["epochSecond"]
            if child_start_time_epoch > end_timestamp:
                end_timestamp = child_start_time_epoch
            if start_timestamp == 0 or child_start_time_epoch < start_timestamp:
                start_timestamp = child_start_time_epoch

            if child["successful"]:
                events_passed += 1
            else:
                events_failed += 1

        table.append(
            [
                parent["eventName"],
                "[ok]" if parent["successful"] else "[fail]",
                events_passed,
                events_failed,
                datetime.fromtimestamp(start_timestamp).isoformat(),
                datetime.fromtimestamp(end_timestamp).isoformat(),
                datetime.fromtimestamp(end_timestamp).isoformat(),
            ]
        )

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
