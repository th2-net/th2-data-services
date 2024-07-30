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

from deprecated.classic import deprecated

from th2_data_services.utils import misc_utils
from typing import Callable, Iterable, List, Literal, Optional

from th2_data_services.utils._types import Th2Event
from th2_data_services.utils.aggregation_classes import FrequencyCategoryTable
from th2_data_services.config import options
from th2_data_services.utils.category import Category


# STREAMING
@deprecated(
    reason='Use "get_category_frequencies2" instead. \n'
    "We want to have unification in functions.\n"
    "Tell DS team if you dont agree or have some ideas."
)
def get_category_frequencies(
    events: Iterable[Th2Event],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = "seconds",
    object_expander=None,
) -> FrequencyCategoryTable:
    """Returns event frequencies based on event category.

    Args:
        events (Iterable[Th2Event]): TH2-Events
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
    return misc_utils.get_objects_frequencies2(
        events,
        categories,
        categorizer,
        # TODO -- we shouldn't know internal structure!!! - epochSeconds
        lambda e: options.EVENT_FIELDS_RESOLVER.get_start_timestamp(e)["epochSecond"],
        aggregation_level=aggregation_level,
        object_expander=object_expander,
    )


# Doesn't use category name now. Category values are table header.
def get_category_frequencies2(
    events: Iterable[Th2Event],
    category: Category,
    aggregation_level: str = "seconds",
    filter_: Optional[Callable] = None,
    gap_mode: Literal[1, 2, 3] = 1,
    zero_anchor: bool = False,
    include_total: bool = True,
) -> FrequencyCategoryTable:
    """Returns event frequencies based on event category.

    For more info please see: https://github.com/th2-net/th2-data-services/blob/dev_2.0.0/documentation/frequencies.md

    Args:
        events (Iterable[Th2Event]): TH2-Events
        category: The name of the category doesn't make sence.
            Used just for unification to use general Category class.
        aggregation_level (Optional, str): Aggregation Level
        filter_: Event filter function
        gap_mode:
            1 - Every range starts with actual event timestamp,
            2 - Ranges are split equally,
            3 - Same as 2, but filled with empty ranges in between
        zero_anchor: If False anchor used is first timestamp from event, if True anchor is 0
        include_total: Will add Total column if True.

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

    Examples:
        It'll return the table like this.
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | timestamp_start   | timestamp_end   | ExecutionReport   | NewOrder   | OrderCancel   |   Total |
        +========+===================+=================+===================+============+===============+=========+
        |        | 2023-08-13        | 2023-08-14      | 1                 | 1          | 2             |       4 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-14        | 2023-08-15      | 1                 | 1          | 2             |       4 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-16        | 2023-08-17      | 0                 | 2          | 3             |       5 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-17        | 2023-08-18      | 1                 | 0          | 1             |       2 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-19        | 2023-08-20      | 1                 | 1          | 0             |       2 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-20        | 2023-08-21      | 0                 | 0          | 2             |       2 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-21        | 2023-08-22      | 1                 | 3          | 0             |       4 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-22        | 2023-08-23      | 1                 | 0          | 0             |       1 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-23        | 2023-08-24      | 0                 | 3          | 0             |       3 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-24        | 2023-08-25      | 0                 | 2          | 1             |       3 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        | count  |                   |                 |                   |            |               |      10 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        | totals |                   |                 | 6                 | 13         | 11            |      30 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+

    """
    return misc_utils.get_objects_frequencies2(
        events,
        categories=[],
        categorizer=category.get_func,
        # TODO -- we shouldn't know internal structure!!! - epochSeconds
        timestamp_function=lambda e: options.EVENT_FIELDS_RESOLVER.get_start_timestamp(e)[
            "epochSecond"
        ],
        aggregation_level=aggregation_level,
        objects_filter=filter_,
        gap_mode=gap_mode,
        zero_anchor=zero_anchor,
        include_total=include_total,
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
def get_type_frequencies(
    events: Iterable[Th2Event], types: List[str], aggregation_level="seconds"
) -> FrequencyCategoryTable:
    """Returns event frequencies based on event type.

    Args:
        events (Iterable[Th2Event]): TH2-Events
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
    return get_category_frequencies(
        events, types, lambda e: options.EVENT_FIELDS_RESOLVER.get_type(e), aggregation_level
    )
