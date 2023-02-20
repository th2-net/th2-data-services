from th2_data_services.utils import misc_utils
from typing import Callable, Dict, List

from th2_data_services.utils.misc_utils import CategoryFrequencies


def get_category_frequencies(
    events: List[Dict], categories: List[str], categorizer: Callable, aggregation_level: str = "seconds"
) -> CategoryFrequencies:
    """Returns event frequencies based on event category.

    categorizer extracts from events some string to calculate its freq
    categories - are values that we want to calculate

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
#    OR maybe better to separate them to modules
#    utils.frequencies.
def get_type_frequencies(events: List[Dict], types: List[str], aggregation_level="seconds") -> CategoryFrequencies:
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
    return get_category_frequencies(events, types, lambda e: e["eventType"], aggregation_level)
