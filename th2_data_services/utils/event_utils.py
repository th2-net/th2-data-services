from typing import Callable, Dict, List, Tuple, Set, Union
from datetime import datetime
from th2_data_services.utils import misc_utils
from th2_data_services import EVENT_FIELDS_RESOLVER, MESSAGE_FIELDS_RESOLVER
import json
from th2_data_services.utils import misc_utils
from typing import Callable, Dict, List, Tuple, Set, Union, Optional
from datetime import datetime
from collections import defaultdict
from tabulate import tabulate

# TODO -
#   1. events: List[Dict] -- should be Iterable[Th2Event], where Th2Event = Dict. It can be changed in the future
#   2. IDEA - it's difficult to understand what you will get when read some functions. I think add examples
#   3. Rename all docstrings word Gets to Returns. That's different things.


# STREAMING
def get_category_frequencies(
    events: List[Dict], categories: List[str], categorizer: Callable, aggregation_level: str = "seconds"
) -> List[List[str]]:
    """Returns event frequencies based on event category.

    Args:
        events (List[Dict]): TH2-Events
        categories (List[str]): Event Categories
        categorizer (Callable): Categorizer Method
        aggregation_level (Optional, str): Aggregation Level

    Returns:
        List[List[str]]

    Example:
        >>> get_category_frequencies(events=events,
                                     categories=["Info", "ModelMatrix"],
                                     categorizer=lambda e: e["eventType"],
                                     aggregation_level="seconds" # Optional
                                     )
        [
            ['timestamp', 'Info', 'ModelMatrix'],
            ['2022-03-16T02:00:00', 4, 0],
            ['2022-03-16T02:00:31', 1, 0],
            ['2022-03-16T02:00:32', 4, 0],
            ...
        ]

    """
    return misc_utils.get_objects_frequencies(
        events,
        categories,
        categorizer,
        lambda e: EVENT_FIELDS_RESOLVER.get_start_timestamp(e)["epochSecond"],
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
def get_type_frequencies(events: List[Dict], types: List[str], aggregation_level="seconds") -> List[List[str]]:
    """Returns event frequencies based on event type.

    Args:
        events (List[Dict]): TH2-Events
        types (List[str]): Event Types
        aggregation_level (Optional, str): Aggregation Level

    Returns:
        List[List[str]]: List Of Frequency Lists

    Example:
        >>> get_type_frequencies(events=events, types=["Info", "ModelMatrix"])
        [
            ['timestamp', 'Info', 'ModelMatrix'],
            ['2022-03-16T02:00:00', 4, 0],
            ['2022-03-16T02:00:31', 1, 0],
            ['2022-03-16T02:00:32', 4, 0],
            ...
        ]
    """
    return get_category_frequencies(events, types, lambda e: EVENT_FIELDS_RESOLVER.get_type(e), aggregation_level)


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
# categorizer - expects that it will return str
def get_category_totals(
    events: List[Dict], categorizer: Callable[[Dict], str], ignore_status: bool = False
) -> Dict[str, int]:
    """Returns dictionary quantities of events for different categories.

    Args:
        events (List[Dict]): TH2-Events
        categorizer (Callable): Categorizer function
        ignore_status (bool): Concatenate status string, defaults to False.

    Returns:
        Dict[str, int]

    Example:
        >>> get_category_totals(events=events,
                                categorizer=lambda e: e["eventType"])
            defaultdict(<class 'int'>, {'Service event [ok]': 9531, 'Info [ok]': 469})
        >>> get_category_totals(events=events,
                                categorizer=lambda e: e["eventType"],
                                ignore_status=True)
            defaultdict(<class 'int'>, {'Service event': 9531, 'Info': 469})
    """
    event_categories = defaultdict(int)
    for event in events:
        category = categorizer(event)
        if not ignore_status:
            status = " [ok]" if EVENT_FIELDS_RESOLVER.get_status(event) else " [fail]"
            category += status
        event_categories[category] += 1

    return event_categories


# USEFUL
# STREAMING
# example
# eu.get_attached_messages_totals(d1)
# defaultdict(<class 'int'>, {'envtn2_msfix5:first': 25262, 'envtn2_jpmfix1:second': 1702, 'env2_gscofixg2:second': 1702,...
def get_attached_messages_totals(events: List[Dict]) -> Dict[str, int]:
    """Returns dictionary quantities of messages attached to events for each stream.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]

    Example:
        >>> get_attached_messages_totals(events=events)
            defaultdict(<class 'int'>, {'envtn2_msfix5:first': 25262, 'envtn2_jpmfix1:second': 1702, ...)
    """
    streams = defaultdict(int)
    for event in events:
        for message_id in EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event):
            key = message_id[: message_id.rindex(":")]
            streams[key] += 1

    return streams


# USEFUL
# STREAMING
def get_attached_message_ids(events: List[Dict]) -> Set[str]:
    """Returns the set of unique message IDs linked to all events.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Set[str]

    Example:
        >>> get_attached_message_ids(events=events)
            {
              'demo_fix5:first:1646738629665873718',
              'demo_fixg2:second:1646736618848913837',
              ...
            }
    """
    return set(message_id for event in events for message_id in EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event))


# USEFUL
# STREAMING
# TODO - It returns only parent events that not present in the events.
#   Perhaps we need to find better name
# we use something similar in our EventTree
def get_prior_parent_ids(events: List[Dict]) -> Set[str]:
    """Returns only parent events that are not present in the events.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Set[str]

    Example:
        >>> get_prior_parent_ids(events=events)
            {
                '009b3122-9ec1-ec11-91bd-ed37395ac9af',
                '014ac1d8-9ed2-ec11-ba0d-13099b4139e8',
                ...
            }
    """
    all_event_ids = set()
    parent_ids = set()
    for event in events:
        parent_id = EVENT_FIELDS_RESOLVER.get_parent_id(event)
        event_id = EVENT_FIELDS_RESOLVER.get_id(event)
        if parent_id is not None and not parent_id in all_event_ids:
            parent_ids.add(parent_id)
        if event_id in parent_ids:
            parent_ids.remove(event_id)
        all_event_ids.add(event_id)

    return parent_ids


# USEFUL
# NOT STREAMING - keeps events
# BE AWARE!! - it can take up all your memory
# O(N*M)
def get_attached_message_ids_index(events: List[Dict]) -> Dict[str, list]:
    """Returns dict of lists of related events by unique message IDs.

    Notes:
        - This object can occupy large amount of memory for big collections of events - use with caution
        Keeps in memory all events that are linked to messages.
        - Event path from root to event, it's a string of event names separated by `/`.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, list]

    Example:
        >>> get_attached_message_ids_index(events=events)
            {
                eventId: {
                    eventName: "example event name",
                    eventPath: "rootName/.../currentEventName"
                },
                ...
            }
    """
    result = defaultdict(list)
    for event in events:
        for message_id in EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event):
            result[message_id].append(event)

    return result


# TODO - USEFULL ??? Do we need ignore status??
# partly the same as get_category_totals and WO ignore status
# Because it's the same we can you get_category_totals inside
#
# STREAMING
def get_type_totals(events: List[Dict]) -> Dict[str, int]:
    """Returns dictionary quantities of events for different event types.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]

    Example:
        >>> get_type_totals(events=events)
            {
                "eventType eventStatus": count,
                ...
            }
    """
    event_types = defaultdict(int)
    for event in events:
        status = " [ok]" if EVENT_FIELDS_RESOLVER.get_status(event) else " [fail] "
        event_type = EVENT_FIELDS_RESOLVER.get_type(event) + status
        event_types[event_type] += 1

    return event_types


# NOT STREAMING
# TODO - USEFUL ???
#   What the example of this? look very rarely need to use
# Will return list! Perhaps it's better to return Data?
def get_some(
    events: List[Dict], event_type: Optional[str], count: int, start: int = 0, failed: bool = False
) -> List[Dict]:
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
        if EVENT_FIELDS_RESOLVER.get_type(event) == event_type:
            if failed and EVENT_FIELDS_RESOLVER.get_status(event):
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


# NOT STREAMING
def get_related_events(events: List[Dict], messages: List[Dict], count: int) -> List[Dict]:
    """Returns limited list of events of linked to any message within specified messages objects collection.

    Args:
        events: TH2-Events
        messages: TH2-Messages
        count: Maximum number of events to extract

    Returns:
        List[Dict]

    Example:
        >>> get_related_events(events=events,
                               messages=messages,
                               count=10)
            [
                {**TH2-Event},
                ...
            ]
    """
    result = []
    msg_ids = set(MESSAGE_FIELDS_RESOLVER.get_id(message) for message in messages)

    for event in events:
        for msg_id in EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event):
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
    """Returns limited list of events of specific category produced by custom categorizer.

    Args:
        events (List[Dict]): TH2-Events
        category (str): Event category to extract
        count (int): Maximum number of events to extract
        categorizer (Callable): Categorizer function
        start (int, optional): Start iteration index, defaults to 0.
        failed (bool, optional): Extract only failed events, defaults to False.

    Returns:
        List[Dict]

    >>> # TODO: example!
        [
            {**TH2-Event},
            ...
        ]
    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if categorizer(event) == category:
            if failed and EVENT_FIELDS_RESOLVER.get_status(event):
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
    """Returns limited list of root events (events without parents).

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
        if EVENT_FIELDS_RESOLVER.get_parent_id(event) is None:
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


# USEFUL
# NOT STREAMING
def get_parents(events: List[Dict], children: List[Dict]) -> List[Dict]:
    """Returns all parent events of linked to any event within specified events objects collection.

    Args:
        events (List[Dict]): TH2-Events
        children (List[Dict]): Extract Parents By Child Events

    Returns:
        List[Dict]

    Example:
        >>> get_parents(events=events, children=subevents)
            [
                {**TH2-Event} # Parent
                ...
            ]
    """
    parent_ids = set(EVENT_FIELDS_RESOLVER.get_parent_id(child) for child in children)
    return [event for event in events if EVENT_FIELDS_RESOLVER.get_id(event) in parent_ids]


# NOT STREAMING
def get_children_from_parent_id(events: List[Dict], parent_id: str, max_events: int) -> Tuple[List[Dict], Dict]:
    """Returns limited list of direct children events.

    Args:
        events (List[Dict]): TH2-Events
        parent_id (str): Parent ID
        max_events (int): Maximum number of events to extract

    Returns:
        Tuple[List[Dict], Dict]: Children Events, Parent Event

    Example:
        >>> get_children_from_parent_id(events=events,
                                        parent_id="demo_parent_id",
                                        max_events=10)
            (
                [{**TH2-Event}, ...], # Child Events
                {**TH2-Event}         # Parent Event
            )
    """
    children = []
    resolved_parent = {}
    counter = 0
    for event in events:
        if EVENT_FIELDS_RESOLVER.get_id(event) == parent_id:
            resolved_parent = event
        if EVENT_FIELDS_RESOLVER.get_parent_id(event) == parent_id:
            children.append(event)
            counter += 1
            if counter == max_events:
                break

    return children, resolved_parent


# NOT STREAMING
def get_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int) -> Tuple[Dict[str, list], int]:
    """Returns limited list of direct children events for each event in parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[str]): TH2-Events
        max_events (int): Maximum number of events to extract from parent

    Returns:
        Tuple(Dict[str, list], int): Parent-Children, Events Count

    Example:
        >>> get_children_from_parents(events=events,
                                      parents=parent_events,
                                      max_events=2)
            (
                {
                    "parentEvent_1": [{**TH2-ChildEvent1, **TH2-ChildEvent2}]
                    "parentEvent_2": [{**TH2-ChildEvent1, **TH2-ChildEvent2}],
                    ...
                },
                child_events_count
            )
    """
    result = {EVENT_FIELDS_RESOLVER.get_id(parent): [] for parent in parents}
    events_count = 0
    for event in events:
        parent_id = EVENT_FIELDS_RESOLVER.get_parent_id(event)
        if parent_id not in result:
            continue
        if len(result[parent_id]) < max_events:
            events_count += 1
            result[parent_id].append(event)

    return result, events_count


# NOT STREAMING
def get_children_from_parents_as_list(events: List[Dict], parents: List[Dict], max_events: int) -> List[Dict]:
    """Returns limited list of direct children events for each event in parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): TH2-Events
        max_events(int): Maximum number of events to extract

    Returns:
        Dict[str, list]: Children Events

    Example:
        >>> get_children_from_parents_as_list(events=events,
                                              parents=parent_events,
                                              max_events=2)
            [
                {**TH2-Parent1_Child1}, {**TH2-Parent1_Child2},
                {**TH2-Parent2_Child2}, {**TH2-Parent2_Child2},
                ...
            ]

    """
    parent_ids = set(EVENT_FIELDS_RESOLVER.get_id(parent) for parent in parents)
    result = []
    parents_counts = defaultdict(int)
    for event in events:
        parent_id = EVENT_FIELDS_RESOLVER.get_parent_id(event)
        if parent_id not in parent_ids:
            continue
        if parents_counts[parent_id] < max_events:
            result.append(event)
        parents_counts[parent_id] += 1

    return result


# NOT STREAMING
def sublist(events: List[Dict], start_time: datetime, end_time: datetime) -> List[Dict]:
    """Filter Events Based On Timeframe.

    Args:
        events (List[Dict]): TH2-Events
        start_time (datetime): Start time
        end_time (datetime): End time

    Returns:
        List[Dict]: Filtered Events.

    Example:
        >>> sublist(events=events,
                    start_time=datetime.fromisoformat("2022-03-16T10:50:16"),
                    end_time=datetime.fromisoformat("2022-03-16T10:53:16"))
            [
                {**TH2-Event},
                ...
            ]
    """
    result = []
    start_time = datetime.timestamp(start_time)
    end_time = datetime.timestamp(end_time)
    for event in events:
        event_time = EVENT_FIELDS_RESOLVER.get_start_timestamp(event)["epochSecond"]
        if start_time <= event_time <= end_time:
            result.append(event)

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
        result[EVENT_FIELDS_RESOLVER.get_id(prev_level)] = {
            "eventName": EVENT_FIELDS_RESOLVER.get_name(prev_level),
            "eventPath": EVENT_FIELDS_RESOLVER.get_name(prev_level),
        }
    while level < depth:
        next_levels = get_children_from_parents_as_list(events, prev_levels, max_level)
        next_levels_count = len(next_levels)
        if next_levels_count == 0:
            break
        level += 1
        print(f"Level {level}: {next_levels_count} events")
        for next_level in next_levels:
            event_id = EVENT_FIELDS_RESOLVER.get_id(next_level)
            parent_id = EVENT_FIELDS_RESOLVER.get_parent_id(next_level)
            result[event_id] = {
                "eventName": EVENT_FIELDS_RESOLVER.get_name(next_level),
                "eventPath": result[parent_id]["eventPath"] + "/" + EVENT_FIELDS_RESOLVER.get_name(next_level),
            }
        prev_levels = next_levels

    return result


# STREAMING
def extract_start_timestamp(event: Dict) -> str:
    """Returns string representation of events timestamp.

    Args:
        event: TH2-Event

    Returns:
        str
    """
    return misc_utils.extract_timestamp(EVENT_FIELDS_RESOLVER.get_start_timestamp(event))


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
    """Prints dictionary quantities of events for different categories.

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
        f"{extract_start_timestamp(event)} > [{'ok' if EVENT_FIELDS_RESOLVER.get_status(event) else 'fail'}] "
        f"Type: {EVENT_FIELDS_RESOLVER.get_type(event)} "
        f"Name: {EVENT_FIELDS_RESOLVER.get_name(event)} "
        f"ID: {EVENT_FIELDS_RESOLVER.get_id(event)} "
        f"Parent:{EVENT_FIELDS_RESOLVER.get_parent_id(event)} "
        f"Body:{EVENT_FIELDS_RESOLVER.get_body(event)}"
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
        categorizer (Callable): Categorizer function
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
def print_children(events: List[Dict], parent_id: str, count: int, verbose: bool = True):
    """Prints limited list of direct children events.

    Args:
        events (List[Dict]): TH2-Events
        parent_id (str): Parent ID
        count (int): Maximum number of events to extract
        verbose (bool): Verbose output, defaults to True.

    """
    records, _ = get_children_from_parent_id(events, parent_id, count)
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
    return misc_utils.print_stats_dict(event_types, return_html=return_html)


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
    table = get_type_frequencies(events, event_types, aggregation_level)
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
        categorizer (Callable): Categorizer function
        aggregation_level (str): Aggregation Level
        return_html: Return HTML Format

    Returns:
        Union[None, str]
    """
    data = get_category_frequencies(events, event_types, categorizer, aggregation_level)
    if return_html:
        return tabulate(data, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(data, headers="firstrow", tablefmt="grid"))
        return None


# NOT STREAMING
def print_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int = 10_000) -> None:
    """Prints limited list of direct children events for each event in parents_list.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): Parent TH2-Events
        max_events (int): Maximum number of events to extract from each parent, default to 10'000

    """
    tree, count = get_children_from_parents(events, parents, max_events)
    print(f"####### Retrieved Children: {count}")
    for parent in parents:
        print(parent)
        print(f">>>>>>> Children: {len(tree[EVENT_FIELDS_RESOLVER.get_id(parent)])}")
        for child in tree[EVENT_FIELDS_RESOLVER.get_id(parent)]:
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
        for child in tree[EVENT_FIELDS_RESOLVER.get_id(parent)]:
            child_start_time_epoch = EVENT_FIELDS_RESOLVER.get_start_timestamp(child)["epochSecond"]
            if child_start_time_epoch > end_timestamp:
                end_timestamp = child_start_time_epoch
            if start_timestamp == 0 or child_start_time_epoch < start_timestamp:
                start_timestamp = child_start_time_epoch

            if EVENT_FIELDS_RESOLVER.get_status(child):
                events_passed += 1
            else:
                events_failed += 1

        table.append(
            [
                EVENT_FIELDS_RESOLVER.get_name(parent),
                "[ok]" if EVENT_FIELDS_RESOLVER.get_status(parent) else "[fail]",
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
