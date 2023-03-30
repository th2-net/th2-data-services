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
) -> FrequencyCategoryTable:  # noqa
    return misc_utils.get_objects_frequencies2(
        messages,
        categories,
        categorizer,
        # TODO -- we shouldn't know internal structure!!! - epochSeconds
        lambda message: options.MESSAGE_FIELDS_RESOLVER.get_timestamp(message)["epochSecond"],
        aggregation_level=aggregation_level,
        object_expander=expand_message,
        objects_filter=filter_,
    )
