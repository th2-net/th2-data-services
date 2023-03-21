from typing import Callable, Dict, Iterable, List, Union, Sequence
from collections import defaultdict

from deprecated.classic import deprecated

from th2_data_services import EVENT_FIELDS_RESOLVER
from th2_data_services.events_tree.events_tree import Th2Event
from th2_data_services.utils.aggregation_classes import CategoryTotal, CategoryTable, \
    TotalCategoryTable
from th2_data_services.utils.total_category_calculator import TotalCategoryCalculator
from th2_data_services.utils.category import Category

"""
These functions return how many events were in some category.
"""


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
# categorizer - expects that it will return str
# def get_category_totals(
#     events: Iterable[Th2Event], categorizer: Callable[[Dict], str], ignore_status: bool = False
# ) -> StatsTotal:
#     """Returns dictionary quantities of events for different categories.
#
#     Args:
#         events (List[Dict]): TH2-Events
#         categorizer (Callable): Categorizer function
#         ignore_status (bool): Concatenate status string, defaults to False.
#
#     Returns:
#         Dict[str, int]
#
#     Example:
#         >>> get_category_totals(events=events,
#                                 categorizer=lambda e: e["eventType"])
#             defaultdict(<class 'int'>, {'Service event [ok]': 9531, 'Info [ok]': 469})
#         >>> get_category_totals(events=events,
#                                 categorizer=lambda e: e["eventType"],
#                                 ignore_status=True)
#             defaultdict(<class 'int'>, {'Service event': 9531, 'Info': 469})
#     """
#     event_categories = defaultdict(int)
#     for event in events:
#         category = categorizer(event)
#         if not ignore_status:
#             status = " [ok]" if EVENT_FIELDS_RESOLVER.get_status(event) else " [fail]"
#             category += status
#         event_categories[category] += 1
#
#     return CategoryTotal(event_categories)

# TODO - we have categorizer and Category now
#   It's a good idea to unite them
@deprecated(reason='Use "get_category_totals2" instead. \n'
                   'It provides more advantages. \n'
                   'Make sure, it has another interface.\n'
                   'Example:\n'
                   '  metrics = [Category("date", lambda m: m["eventType"])] \n '
                   '  totals.get_category_totals2(events, metrics).sort_by("date")')
def get_category_totals(
        events: Iterable[Th2Event], categorizer: Callable[[Dict], str], ignore_status: bool = False
) -> CategoryTotal:
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

    return CategoryTotal(event_categories)


# TODO - it will be renamed to get_category_totals
def get_category_totals2(
        events: Iterable[Th2Event],
        categories: List[Category],
        # order=None
) -> TotalCategoryTable:
    """More advanced totals with multiple columns.

    Examples:
        metrics = [
            Category('date', lambda m: Th2TimestampConverter.to_datetime(m['startTimestamp']).date()) ]
        totals.get_category_totals2(events, metrics).sort_by('date')

    Args:
        events:
        categories:

    Returns:

    """

    # if order is None:
    #     order = [metrics]
    # else:
    #     order = [order]
    ctc = TotalCategoryCalculator(categories, [categories])
    ctc.handle_objects(events)
    tct = ctc.get_table(categories)
    return tct


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
def get_attached_messages_totals(events: Iterable[Th2Event]) -> CategoryTotal:
    """Returns dictionary quantities of messages attached to events for each stream.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]

    Example:
        >>> get_attached_messages_totals(events=events)
            defaultdict(<class 'int'>, {'envtn2_msfix5:first': 25262,
                                        'envtn2_jpmfix1:second': 1702, ...)
    """
    streams = defaultdict(int)
    for event in events:
        for message_id in EVENT_FIELDS_RESOLVER.get_attached_messages_ids(event):
            key = message_id[: message_id.rindex(":")]
            streams[key] += 1

    return CategoryTotal(streams)


# TODO - USEFULL ??? Do we need ignore status??
# partly the same as get_category_totals and WO ignore status
# Because it's the same we can you get_category_totals inside
#
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
def get_type_totals(events: Iterable[Th2Event]) -> CategoryTotal:
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
        status = " [ok]" if event["successful"] else " [fail] "
        event_type = event["eventType"] + status
        event_types[event_type] += 1

    return CategoryTotal(event_types)
