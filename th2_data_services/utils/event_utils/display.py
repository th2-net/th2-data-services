from typing import Callable, Dict, List, Union
from datetime import datetime
from tabulate import tabulate
from typing import List, Dict, Callable

from th2_data_services.utils.event_utils.event_utils import extract_start_timestamp, get_some
from th2_data_services.utils.event_utils.select import (
    get_children_from_parents,
    get_events_by_category,
    get_roots,
    get_children_from_parent_id,
)


# TODO
#   COMMENTED - because we don't need it more. We will return classes that have good representation!
# def print_attached_messages_totals(events: List[Dict], return_html: bool = False) -> Union[None, str]:
#     """Prints Dictionary quantities of messages attached to events for each stream + direction.
#
#     Args:
#         events (List[Dict]): TH2-Events
#         return_html (bool): Return HTML Format
#
#     """
#     data = get_attached_messages_totals(events)
#     return misc_utils.print_stats_dict(data, return_html)


# TODO
#   COMMENTED - because we don't need it more. We will return classes that have good representation!
# def print_category_totals(
#     events: List[Dict], categorizer: Callable, return_html: bool = False, ignore_status: bool = False
# ) -> Union[None, str]:
#     """Prints dictionary quantities of events for different categories.
#
#     Args:
#         events (List[Dict]): TH2-Events
#         categorizer (Callable): Categorizer Method
#         return_html (bool): Return HTML Format, defaults to False
#         ignore_status (bool): Get status of events, defaults to False
#
#     Returns:
#         Union[None, str]
#     """
#     data = get_category_totals(events, categorizer, ignore_status=ignore_status)
#     return misc_utils.print_stats_dict(data, return_html)


# STREAMING
def print_event(event: Dict) -> None:
    """Prints event in human-readable format.

    Args:
        event (List[Dict]): TH2-Events

    """
    print(
        f"{extract_start_timestamp(event)} > [{'ok' if event['successful'] else 'fail'}] "
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


# TODO
#   COMMENTED - because we don't need it more. We will return classes that have good representation!
# STREAMING
# TODO - bad function, that not only prints but also gets
#   If we want to have pretty look, we can implement __repr__ functions
# def print_type_frequencies(
#     events: List[Dict], event_types: List[str], aggregation_level: str = "seconds", return_html=False
# ) -> Union[None, str]:
#     """Prints table of events per seconds or each second when there were events within events stream.
#
#     Args:
#         events: TH2-Events
#         event_types: List of event types to analyze
#         aggregation_level: Aggregation level
#         return_html: Return HTML format, defaults to False
#
#     """
#     table = get_type_frequencies(events, event_types, aggregation_level)
#     if return_html:
#         return tabulate(table, headers="firstrow", tablefmt="html")
#     else:
#         print(tabulate(table, headers="firstrow", tablefmt="grid"))
#
#
# # STREAMING
# # TODO - takes event_types - but it should be categiries
#
# def print_category_frequencies(
#     events: List[Dict],
#     event_types: List[str],
#     categorizer: Callable,
#     aggregation_level: str = "seconds",
#     return_html: bool = False,
# ) -> Union[None, str]:
#     """Prints table of events per seconds or each second when there were events within events stream.
#
#     Args:
#         events (List[Dict]): TH2-Events
#         event_types (List[str]): Event Types To Extract
#         categorizer (Callable): Categorizer function
#         aggregation_level (str): Aggregation Level
#         return_html: Return HTML Format
#
#     Returns:
#         Union[None, str]
#     """
#     data = get_category_frequencies(events, event_types, categorizer, aggregation_level)
#     if return_html:
#         return tabulate(data, headers="firstrow", tablefmt="html")
#     else:
#         print(tabulate(data, headers="firstrow", tablefmt="grid"))
#         return None
# def print_type_totals(events: List[Dict], return_html: bool = False) -> Union[None, str]:
#     """Prints dictionary quantities of events for different event types.
#
#     Args:
#         events (List[Dict]): TH2-Events
#         return_html (bool): HTML format, defaults to False
#
#     Returns:
#         Union[None, str]
#     """
#     event_types = get_type_totals(events)
#     return misc_utils.print_stats_dict(event_types, return_html=return_html)
