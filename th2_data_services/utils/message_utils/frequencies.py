# from th2_data_services import MESSAGE_FIELDS_RESOLVER
from typing import Callable, Iterable, List
from th2_data_services.utils import misc_utils
from th2_data_services.utils.message_utils.message_utils import expand_message
from th2_data_services.utils.aggregation_classes import FrequencyCategoryTable

from th2_data_services.config import options

Th2Message = dict

# NOT STREAMABLE
def get_category_frequencies(
    messages: Iterable[Th2Message],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = "seconds",
    filter_: Callable = None,
    gap_mode: int = 1,
    zero_anchor: bool = False,
) -> FrequencyCategoryTable:  # noqa
    """Returns message frequencies based on categorizer.

    Returns timestamps in UTC format.

    Args:
        messages: Messages stored in any iterable
        categories: Categories list
        categorizer: Categorizer function
        aggregation_level: Aggregation level
        filter: Message filter function
        gap_mode: 1 - Every range starts with actual message timestamp, 2 - Ranges are split equally, 3 - Same as 2, but filled with empty ranges in between
        zero_anchor: If False anchor used is first timestamp from message, if True anchor is 0

    Returns:
        List[List]
    """
    return misc_utils.get_objects_frequencies2(
        messages,
        categories,
        categorizer,
        # TODO -- we shouldn't know internal structure!!! - epochSeconds
        lambda message: options.MESSAGE_FIELDS_RESOLVER.get_timestamp(message)["epochSecond"],
        aggregation_level=aggregation_level,
        object_expander=expand_message,
        objects_filter=filter_,
        gap_mode=gap_mode,
        zero_anchor=zero_anchor,
    )
