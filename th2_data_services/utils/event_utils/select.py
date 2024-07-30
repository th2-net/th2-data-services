# The module for selecting events by some rules
from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict, Iterable, Set, Tuple

from deprecated.classic import deprecated

from th2_data_services.utils._types import Th2Event
from th2_data_services.config import options


# TODO - THEY ALL ARE NOT STREAMING!!
#   1. what about iter functions or return Data obj?  The second one sounds better


def get_related_events(
    events: Iterable[Th2Event], messages: Iterable[Th2Event], count: int
) -> Iterable[Th2Event]:
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
    msg_ids = set(options.MESSAGE_FIELDS_RESOLVER.get_id(message) for message in messages)

    for event in events:
        for msg_id in options.EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event):
            if msg_id in msg_ids:
                result.append(event)
                if len(result) == count:
                    return result

    return result


# TODO - duplicates get_some (get_events)
def get_events_by_category(
    events: Iterable[Th2Event],
    category: str,
    count: int,
    categorizer: Callable,
    start=0,
    failed=False,
) -> Iterable[Th2Event]:
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
            if failed and options.EVENT_FIELDS_RESOLVER.get_status(event):
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


def get_roots(events: Iterable[Th2Event], count: int, start: int = 0) -> Iterable[Th2Event]:
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
        if options.EVENT_FIELDS_RESOLVER.get_parent_id(event) is None:
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


def get_parents(events: Iterable[Th2Event], children: Iterable[Th2Event]) -> Iterable[Th2Event]:
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
    parent_ids = set(options.EVENT_FIELDS_RESOLVER.get_parent_id(child) for child in children)
    return [event for event in events if options.EVENT_FIELDS_RESOLVER.get_id(event) in parent_ids]


def get_children_from_parent_id(
    events: Iterable[Th2Event], parent_id: str, max_events: int
) -> Tuple[Iterable[Th2Event], Th2Event]:
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
        if options.EVENT_FIELDS_RESOLVER.get_id(event) == parent_id:
            resolved_parent = event
        if options.EVENT_FIELDS_RESOLVER.get_parent_id(event) == parent_id:
            children.append(event)
            counter += 1
            if counter == max_events:
                break

    return children, resolved_parent


def get_children_from_parents(
    events: Iterable[Th2Event], parents: Iterable[Th2Event], max_events: int
) -> Tuple[Dict[str, list], int]:
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
    result = {options.EVENT_FIELDS_RESOLVER.get_id(parent): [] for parent in parents}
    events_count = 0
    for event in events:
        parent_id = options.EVENT_FIELDS_RESOLVER.get_parent_id(event)
        if parent_id not in result:
            continue
        if len(result[parent_id]) < max_events:
            events_count += 1
            result[parent_id].append(event)

    return result, events_count


@deprecated("Use `get_children_from_parents` instead")
def get_children_for_events_list(evnts, parents_list, max_events):  # noqa
    return get_children_from_parents(evnts, parents_list, max_events)


def get_children_from_parents_as_list(
    events: Iterable[Th2Event], parents: Iterable[Th2Event], max_events: int
) -> Iterable[Th2Event]:
    """Returns limited list of direct children events for each event in parents.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        parents (Iterable[Th2Event]): TH2-Events
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
    parent_ids = set(options.EVENT_FIELDS_RESOLVER.get_id(parent) for parent in parents)
    result = []
    parents_counts = defaultdict(int)
    for event in events:
        parent_id = options.EVENT_FIELDS_RESOLVER.get_parent_id(event)
        if parent_id not in parent_ids:
            continue
        if parents_counts[parent_id] < max_events:
            result.append(event)
        parents_counts[parent_id] += 1

    return result


def sublist(
    events: Iterable[Th2Event], start_time: datetime, end_time: datetime
) -> Iterable[Th2Event]:
    """Filter Events Based On Timeframe.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        start_time (datetime): Start time
        end_time (datetime): End time

    Returns:
        Iterable[Th2Event]: Filtered Events.

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
        event_time = options.EVENT_FIELDS_RESOLVER.get_start_timestamp(event)["epochSecond"]
        if start_time <= event_time <= end_time:
            result.append(event)

    return result


# USEFUL
# NOT STREAMING
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
def get_attached_message_ids(events: Iterable[Th2Event]) -> Set[str]:
    """Returns the set of unique message IDs linked to all events.

    Args:
        events (Iterable[Th2Event]): TH2-Events

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
    return set(
        message_id
        for event in events
        for message_id in options.EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event)
    )


# USEFUL
# NOT STREAMING
# TODO - NOT-READY -- event["parentEventId, eventId"] should be updated by resolver
# TODO - It returns only parent events that not present in the events.
#   Perhaps we need to find better name
# we use something similar in our EventTree
def get_prior_parent_ids(events: Iterable[Th2Event]) -> Set[str]:
    """Returns only parent events that are not present in the events.

    Args:
        events (Iterable[Th2Event]): TH2-Events

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
        parent_id = options.EVENT_FIELDS_RESOLVER.get_parent_id(event)
        event_id = options.EVENT_FIELDS_RESOLVER.get_id(event)
        if parent_id is not None and parent_id not in all_event_ids:
            parent_ids.add(parent_id)
        if event_id in parent_ids:
            parent_ids.remove(event_id)
        all_event_ids.add(event_id)

    return parent_ids


# USEFUL
# NOT STREAMING - keeps events
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
# BE AWARE!! - it can take up all your memory
# O(N*M)
def get_attached_message_ids_index(events: Iterable[Th2Event]) -> Dict[str, list]:
    """Returns dict of lists of related events by unique message IDs.

    Notes:
        - This object can occupy large amount of memory for big collections of events - use with caution
        Keeps in memory all events that are linked to messages.
        - Event path from root to event, it's a string of event names separated by `/`.

    Args:
        events (Iterable[Th2Event]): TH2-Events

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
        for message_id in options.EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event):
            result[message_id].append(event)

    return result
