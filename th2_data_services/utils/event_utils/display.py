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

from typing import Iterable, Union
from datetime import datetime
from tabulate import tabulate
from typing import Callable

from th2_data_services.utils.event_utils.event_utils import extract_start_timestamp, get_some
from th2_data_services.utils.event_utils.select import (
    get_children_from_parents,
    get_events_by_category,
    get_roots,
    get_children_from_parent_id,
)
from th2_data_services.utils._types import Th2Event

from th2_data_services.config import options


# TODO
#   COMMENTED - because we don't need it more. We will return classes that have good representation!
# def print_attached_messages_totals(events: Iterable[Th2Event], return_html: bool = False) -> Union[None, str]:
#     """Prints Dictionary quantities of messages attached to events for each stream + direction.
#
#     Args:
#         events (Iterable[Th2Event]): TH2-Events
#         return_html (bool): Return HTML Format
#
#     """
#     data = get_attached_messages_totals(events)
#     return misc_utils.print_stats_dict(data, return_html)


# TODO
#   COMMENTED - because we don't need it more. We will return classes that have good representation!
# def print_category_totals(
#     events: Iterable[Th2Event], categorizer: Callable, return_html: bool = False, ignore_status: bool = False
# ) -> Union[None, str]:
#     """Prints dictionary quantities of events for different categories.
#
#     Args:
#         events (Iterable[Th2Event]): TH2-Events
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
def print_event(event: Th2Event) -> None:
    """Prints event in human-readable format.

    Args:
        event (Th2Event): TH2-Event

    """
    print(
        f"{extract_start_timestamp(event)} > [{'ok' if options.EVENT_FIELDS_RESOLVER.get_status(event) else 'fail'}] "
        f"Type: {options.EVENT_FIELDS_RESOLVER.get_type(event)} "
        f"Name: {options.EVENT_FIELDS_RESOLVER.get_name(event)} "
        f"ID: {options.EVENT_FIELDS_RESOLVER.get_id(event)} "
        f"Parent:{options.EVENT_FIELDS_RESOLVER.get_parent_id(event)} "
        f"Body:{options.EVENT_FIELDS_RESOLVER.get_body(event)}"
    )


# NOT STREAMING
# PREV name print_some_raw
def print_events_raw(
    events: Iterable[Th2Event], event_type: str, count: int, start: int = 0, failed: bool = False
) -> None:
    """Prints limited list of events of specific eventType in dictionary format.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        event_type (set): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    """
    records = get_some(events, event_type, count, start, failed)
    for r in records:
        print(r)


# NOT STREAMING
def print_some(
    events: Iterable[Th2Event], event_type: str, count: int, start: int = 0, failed: bool = False
) -> None:
    """Prints limited list of events of specific eventType in human-readable format.

    Args:
        events (Iterable[Th2Event]): TH2-Events
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
    events: Iterable[Th2Event],
    category: str,
    count: int,
    categorizer: Callable,
    start: int = 0,
    failed: bool = False,
) -> None:
    """Print limited events by category.

    Args:
        events (Iterable[Th2Event]): TH2-Events
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
def print_roots(events: Iterable[Th2Event], count: int, start: int = 0) -> None:
    """Prints limited list of root events (events without parents).

    Args:
        events (Iterable[Th2Event]): TH2-Events
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.

    """
    records = get_roots(events, count, start)
    for r in records:
        print_event(r)


# STREAMING
def print_children(events: Iterable[Th2Event], parent_id: str, count: int, verbose: bool = True):
    """Prints limited list of direct children events.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        parent_id (str): Parent ID
        count (int): Maximum number of events to extract
        verbose (bool): Verbose output, defaults to True.

    """
    records, _ = get_children_from_parent_id(events, parent_id, count)
    fprint = print_event if verbose is True else print
    for r in records:
        fprint(r)


# NOT STREAMING
def print_children_from_parents(
    events: Iterable[Th2Event], parents: Iterable[Th2Event], max_events: int = 10_000
) -> None:
    """Prints limited list of direct children events for each event in parents_list.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        parents (Iterable[Th2Event]): Parent TH2-Events
        max_events (int): Maximum number of events to extract from each parent, default to 10'000

    """
    tree, count = get_children_from_parents(events, parents, max_events)
    print(f"####### Retrieved Children: {count}")
    for parent in parents:
        print(parent)
        print(f">>>>>>> Children: {len(tree[options.EVENT_FIELDS_RESOLVER.get_id(parent)])}")
        for child in tree[options.EVENT_FIELDS_RESOLVER.get_id(parent)]:
            print_event(child)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


# NOT STREAMING
def print_children_stats_from_parents(
    events: Iterable[Th2Event],
    parents: Iterable[Th2Event],
    max_events: int = 10_000,
    return_html: bool = False,
) -> Union[None, str]:
    """Prints statistics with number of children and their duration for each event in parents_list.

    Args:
        events (Iterable[Th2Event]): TH2-Events
        parents (Iterable[Th2Event]): Parent TH2-Events
        max_events (int): Maximum number of events to extract, default to 10'000
        return_html (bool): Return HTML format, defaults to False

    """
    tree, _ = get_children_from_parents(events, parents, max_events)
    table = [
        ["eventName", "status", "eventId", "child_pass", "child_fail", "start", "end"]
    ]  # Header
    for parent in parents:
        start_timestamp, end_timestamp = 0, 0
        events_passed, events_failed = 0, 0
        for child in tree[options.EVENT_FIELDS_RESOLVER.get_id(parent)]:
            child_start_time_epoch = options.EVENT_FIELDS_RESOLVER.get_start_timestamp(child)[
                "epochSecond"
            ]
            if child_start_time_epoch > end_timestamp:
                end_timestamp = child_start_time_epoch
            if start_timestamp == 0 or child_start_time_epoch < start_timestamp:
                start_timestamp = child_start_time_epoch

            if options.EVENT_FIELDS_RESOLVER.get_status(child):
                events_passed += 1
            else:
                events_failed += 1

        table.append(
            [
                options.EVENT_FIELDS_RESOLVER.get_name(parent),
                "[ok]" if options.EVENT_FIELDS_RESOLVER.get_status(parent) else "[fail]",
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
#     events: Iterable[Th2Event], event_types: List[str], aggregation_level: str = "seconds", return_html=False
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
