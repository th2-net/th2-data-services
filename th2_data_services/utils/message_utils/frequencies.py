# from th2_data_services import MESSAGE_FIELDS_RESOLVER
from typing import Callable, Iterable, List
from th2_data_services.utils import misc_utils
from th2_data_services.utils.message_utils.message_utils import expand_message
from th2_data_services.utils.aggregation_classes import FrequencyCategoryTable

from th2_data_services.config import options

Th2Message = dict

'''
    Example:
        msgs = [
            {
                "timestamp":{"epochSecond":1682296588}, # 2023-04-24T00:36:28
                "messageType": "ERROR"
            },
            {
                "timestamp":{"epochSecond":1682296587}, # 2023-04-24T00:36:27
                "messageType": "ERROR"
            },
            {
                "timestamp":{"epochSecond":1682293587}, # 2023-04-23T23:46:27
                "messageType": "ERROR"
            },
            {
                "timestamp":{"epochSecond":1682296559}, # 2023-04-24T00:35:59
                "messageType": "ERROR"
            }
        ]

        table = message_utils.frequencies.get_category_frequencies(msgs,[],lambda a:a['messageType'],aggregation_level='5sec')

        +---------------------+---------+
        | timestamp           |   ERROR |
        +=====================+=========+
        | 2023-04-23T23:46:23 |       1 |
        +---------------------+---------+
        | 2023-04-24T00:35:58 |       1 |
        +---------------------+---------+
        | 2023-04-24T00:36:23 |       1 |
        +---------------------+---------+
        | 2023-04-24T00:36:28 |       1 |
        +---------------------+---------+

        table = message_utils.frequencies.get_category_frequencies(msgs,[],lambda a:a['messageType'],aggregation_level='30s')

        +---------------------+---------+
        | timestamp           |   ERROR |
        +=====================+=========+
        | 2023-04-23T23:45:58 |       1 |
        +---------------------+---------+
        | 2023-04-24T00:35:58 |       2 |
        +---------------------+---------+
        | 2023-04-24T00:36:28 |       1 |
        +---------------------+---------+

        table = message_utils.frequencies.get_category_frequencies(msgs,[],lambda a:a['messageType'],aggregation_level='2min')

        +------------------+---------+
        | timestamp        |   ERROR |
        +==================+=========+
        | 2023-04-23T23:46 |       1 |
        +------------------+---------+
        | 2023-04-24T00:34 |       1 |
        +------------------+---------+
        | 2023-04-24T00:36 |       2 |
        +------------------+---------+

        table = message_utils.frequencies.get_category_frequencies(msgs,[],lambda a:a['messageType'],aggregation_level='3h')

        +------------------+---------+
        | timestamp        |   ERROR |
        +==================+=========+
        | 2023-04-23T21:00 |       1 |
        +------------------+---------+
        | 2023-04-24T00:00 |       3 |
        +------------------+---------+

        table = message_utils.frequencies.get_category_frequencies(msgs,[],lambda a:a['messageType'],aggregation_level='4d')

        +-------------+---------+
        | timestamp   |   ERROR |
        +=============+=========+
        | 2023-04-20  |       1 |
        +-------------+---------+
        | 2023-04-24  |       3 |
        +-------------+---------+
'''
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
    return misc_utils.get_objects_frequencies2(
        messages,
        categories,
        categorizer,
        # TODO -- we shouldn't know internal structure!!! - epochSeconds
        lambda message: options.MESSAGE_FIELDS_RESOLVER.get_timestamp(message)["epochSecond"],
        aggregation_level=aggregation_level,
        object_expander=expand_message,
        objects_filter=filter_,
        gap_mode = gap_mode,
        zero_anchor = zero_anchor,
    )
