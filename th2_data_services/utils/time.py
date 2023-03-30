#  Copyright 2023 Exactpro (Exactpro Systems Limited)
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
from datetime import datetime
from typing import Dict, Union


# TODO - looks ok, but it's better to add such feature to utils.converters
from deprecated.classic import deprecated


def extract_timestamp(timestamp_element: Dict) -> str:
    """Extracts timestamp from argument.

    Args:
        timestamp_element:

    Returns:
        str representation of th2-timestamp(protobuf) e.g. 2023-03-09T05:37:53.263895000
    """
    timestamp = datetime.fromtimestamp(timestamp_element["epochSecond"])
    return f"{timestamp.isoformat()}.{str(timestamp_element['nano']).zfill(9)}"


@deprecated("Use `extract_timestamp` instead")
def extract_time_string(timestamp_element):
    return extract_timestamp(timestamp_element)


# TODO - to be honest, the name of the function is difficult
def time_interval_filter_seconds_precision(
    timestamp_element: Dict, start_timestamp: Union[int, float], end_timestamp: Union[int, float]
) -> bool:
    """Returns if th2-timestamp within time range.

    Args:
        timestamp_element: Timestamp element
        start_timestamp: Start timestamp
        end_timestamp: End timestamp

    Returns:
        bool
    """
    return start_timestamp <= timestamp_element["epochSecond"] <= end_timestamp


def timestamp_delta_us(start_timestamp: Dict, end_timestamp: Dict) -> float:
    """Returns timestamp delta in milliseconds.

    Args:
        start_timestamp: Start timestamp
        end_timestamp: End timestamp

    Returns:
        float
    """
    seconds_delta = (end_timestamp["epochSecond"] - start_timestamp["epochSecond"]) * 1000000
    nano_delta = (end_timestamp["nano"] - start_timestamp["nano"]) / 1000
    return seconds_delta + nano_delta


# TODO - looks ok, but we need to think about unified timestamps
def time_slice_object_filter(timestamp_field: Dict, timestamp_iso: str, duration_seconds: int):  # noqa
    """Filter elements that from time moment  A to  A+duration_seconds.

    Args:
        timestamp_field:
        timestamp_iso:
        duration_seconds:

    Returns:

    """
    ts1 = datetime.fromisoformat(timestamp_iso).timestamp()
    ts2 = ts1 + duration_seconds

    return lambda obj: time_interval_filter_seconds_precision(obj[timestamp_field], ts1, ts2)


# TODO - add possibility to provide  `aggregation_level` as int (number of seconds)
def timestamp_aggregation_key(
    global_anchor_timestamp: int, timestamp: int, aggregation_level: str = "seconds"
) -> int:  # noqa
    """TODO: Add docstings

    Args:
        global_anchor_timestamp:
        timestamp:
        aggregation_level:  e.g. 1s, 1sec, seconds, 10m, 10min, 10h, 10hour, 1d, 2day

    Returns:

    """
    if aggregation_level == "seconds":
        return timestamp

    aggregation_levels = {
        "seconds": 1,
        "minutes": 60,
        "hours": 3600,
        # TODO - should be dynamic part
        "30min": 1800,
        "1min": 60,
        "5min": 300,
        "10sec": 10,
        "30sec": 30,
    }

    if aggregation_level not in aggregation_levels:
        if aggregation_level.endswith("sec"):
            num = aggregation_level.split("sec")[0]
            dynamic_aggr_level = int(num)

        elif aggregation_level.endswith("s"):
            num = aggregation_level.split("s")[0]
            dynamic_aggr_level = int(num)

        elif aggregation_level.endswith("min"):
            num = aggregation_level.split("min")[0]
            dynamic_aggr_level = int(num) * 60

        elif aggregation_level.endswith("m"):
            num = aggregation_level.split("m")[0]
            dynamic_aggr_level = int(num) * 60

        elif aggregation_level.endswith("hour"):
            num = aggregation_level.split("hour")[0]
            dynamic_aggr_level = int(num) * 3600

        elif aggregation_level.endswith("h"):
            num = aggregation_level.split("h")[0]
            dynamic_aggr_level = int(num) * 3600

        elif aggregation_level.endswith("day"):
            num = aggregation_level.split("day")[0]
            dynamic_aggr_level = int(num) * 3600 * 24

        elif aggregation_level.endswith("d"):
            num = aggregation_level.split("d")[0]
            dynamic_aggr_level = int(num) * 3600 * 24

        else:
            raise KeyError(f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}")
        aggregation_levels[aggregation_level] = dynamic_aggr_level

    try:
        interval = aggregation_levels[aggregation_level]
    except KeyError:
        raise KeyError(f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}")

    return global_anchor_timestamp + interval * ((timestamp - global_anchor_timestamp) // interval)
