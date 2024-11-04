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

from datetime import datetime, timezone
from functools import wraps, partial
from typing import Dict, Union, Callable
from deprecated.classic import deprecated
import time as time_
from th2_data_services.utils.converters import Th2TimestampConverter, DatetimeConverter


def extract_timestamp(timestamp_element: Dict) -> str:
    """Returns datetime string in the format: 2023-10-02T10:47:20.413072000."""
    return Th2TimestampConverter.to_datetime_str(timestamp_element)


@deprecated("Use `extract_timestamp` instead")
def extract_time_string(timestamp_element) -> str:
    """Extracts timestamp from argument.

    Args:
        timestamp_element:

    Returns:
        str representation of th2-timestamp(protobuf) e.g. 2023-03-09T05:37:53.263895000
    """
    return extract_timestamp(timestamp_element)


# TODO - to be honest, the name of the function is difficult
def time_interval_filter_seconds_precision(
    timestamp_element: Dict, start_timestamp: Union[int, float], end_timestamp: Union[int, float]
) -> bool:
    """Returns if th2-timestamp within time range.

    Please note:
        It takes SECONDS only!

    Args:
        timestamp_element: ProtobufTimestamp dict.
        start_timestamp: Start timestamp in `unix time` format.
        end_timestamp: End timestamp in `unix time` format.

    Returns:
        bool
    """
    return start_timestamp <= timestamp_element["epochSecond"] <= end_timestamp


def timestamp_delta_us(start_timestamp: Dict, end_timestamp: Dict) -> int:
    """Returns timestamp delta in microseconds.

    Args:
        start_timestamp: Start timestamp
        end_timestamp: End timestamp

    Returns:
        int
    """
    st_seconds, st_nanoseconds = Th2TimestampConverter.parse_timestamp_int(start_timestamp)
    et_seconds, et_nanoseconds = Th2TimestampConverter.parse_timestamp_int(end_timestamp)

    seconds_delta = (et_seconds - st_seconds) * 1000000
    nano_delta = (et_nanoseconds - st_nanoseconds) / 1000
    return seconds_delta + nano_delta


def time_slice_object_filter(
    timestamp_field: str, start_timestamp_iso: str, duration_seconds: int
) -> Callable:  # noqa
    """Returns filter function for `Data.filter` method.

    Filter elements that from time moment `A` to `A+duration_seconds`.

    Args:
        timestamp_field: expects the field name that contains ProtobufTimestamp
            It usually 'timestamp' field.
        start_timestamp_iso: string in the ISO 8601 format.
            Example: 2009-05-28T16:15:00 or 2021-12-25
            Note: It cannot take strings with `Z` in the end.
        duration_seconds: seconds.

    Returns:
        Filter function.

    Examples:
        1. data.filter(time_slice_object_filter('startTimestamp', '2009-05-28T16:15:00, 300))
    """
    # TODO
    #   1. looks ok, but we need to think about unified timestamps
    # FixMe
    #   1. timestamp_field -- the problem here if the field is placed not in the root of the dict.
    #   2. it expects, that `obj[timestamp_field]` == Th2Timestamp

    ts1 = DatetimeConverter.to_seconds(datetime.fromisoformat(start_timestamp_iso))
    ts2 = ts1 + duration_seconds

    # FIXME
    #   time_interval_filter_seconds_precision require ProtobufTimestamp var as
    #   a first argument now.
    #
    #   TODO - We should do our methods universal!
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
        "days": 86400,
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
            raise KeyError(
                f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}"
            )
        aggregation_levels[aggregation_level] = dynamic_aggr_level

    try:
        interval = aggregation_levels[aggregation_level]
    except KeyError:
        raise KeyError(
            f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}"
        )

    return global_anchor_timestamp + interval * ((timestamp - global_anchor_timestamp) // interval)


def _timestamp_rounded_down(timestamp: int, aggregation_level: str = "seconds"):
    """Extracts timestamp rounded down to aggeegation level type.

    Args:
        timestamp: Timestamp in epoch seconds
        aggregation_level: String of aggregation level like: "5s", "2d", "3m", "hours"

    Returns:
        Rounded down timestamp to aggregation level, for example: If timestamp is equivalent to 2023-04-05T23:12:15 and aggregation level is "5d"
        function will return timestamp equivalent to 2023-04-05
    """
    dynamic_aggr_level = 1
    aggregation_levels = {
        "seconds": 1,
        "minutes": 60,
        "hours": 3600,
        "days": 86400,
        # TODO - should be dynamic part
        "30min": 60,
        "1min": 60,
        "5min": 60,
        "10sec": 1,
        "30sec": 1,
    }

    if aggregation_level not in aggregation_levels:
        if aggregation_level.endswith("sec") or aggregation_level.endswith("s"):
            dynamic_aggr_level = 1

        elif aggregation_level.endswith("min") or aggregation_level.endswith("m"):
            dynamic_aggr_level = 60

        elif aggregation_level.endswith("hour") or aggregation_level.endswith("h"):
            dynamic_aggr_level = 3600

        elif aggregation_level.endswith("day") or aggregation_level.endswith("d"):
            dynamic_aggr_level = 86400

        else:
            raise KeyError(
                f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}"
            )
        aggregation_levels[aggregation_level] = dynamic_aggr_level

    try:
        dynamic_aggr_level = aggregation_levels[aggregation_level]
    except KeyError:
        raise KeyError(
            f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}"
        )

    return (timestamp // dynamic_aggr_level) * dynamic_aggr_level


def _round_timestamp_string_aggregation(timestamp: int, aggregation_level: str = "seconds"):
    """Returns timestamp string rounded down to aggeegation level type.

    Args:
        timestamp: Timestamp in epoch seconds
        aggregation_level: String of aggregation level like: "5s", "2d", "3m", "hours"

    Returns:
        Rounded down timestamp string to aggregation level, for example: If timestamp is equivalent to 2023-04-05T23:12:15 and aggregation level is "5d"
        function will return string 2023-04-05
    """
    # First check full strings to ensure .endswith("s") doesn't catch it.
    if aggregation_level == "seconds":
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    if aggregation_level == "minutes" or aggregation_level == "hours":
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M")

    if aggregation_level == "days":
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    if aggregation_level.endswith("sec") or aggregation_level.endswith("s"):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    if aggregation_level.endswith("min") or aggregation_level.endswith("m"):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M")

    if aggregation_level.endswith("hour") or aggregation_level.endswith("h"):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M")

    if aggregation_level.endswith("day") or aggregation_level.endswith("d"):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    raise KeyError("Invalid aggregation level")


def _time_str_to_seconds(time_str: str):
    """Returns the amount of seconds in aggregation level.

    Args:
        time_str: Aggregation level string like: "5s", "2d", "3m", "hours"

    Returns:
        Number of seconds in string, for example: "5s" returns 5, "3m" returns 180 and etc.
    """
    if time_str == "seconds":
        return 1

    if time_str == "minutes":
        return 60

    if time_str == "hours":
        return 3600

    if time_str == "days":
        return 86400

    if time_str.endswith("sec"):
        num = time_str.split("sec")[0]
        return int(num)

    elif time_str.endswith("s"):
        num = time_str.split("s")[0]
        return int(num)

    elif time_str.endswith("min"):
        num = time_str.split("min")[0]
        return int(num) * 60

    elif time_str.endswith("m"):
        num = time_str.split("m")[0]
        return int(num) * 60

    elif time_str.endswith("hour"):
        num = time_str.split("hour")[0]
        return int(num) * 3600

    elif time_str.endswith("h"):
        num = time_str.split("h")[0]
        return int(num) * 3600

    elif time_str.endswith("day"):
        num = time_str.split("day")[0]
        return int(num) * 3600 * 24

    elif time_str.endswith("d"):
        num = time_str.split("d")[0]
        return int(num) * 3600 * 24

    raise KeyError("Invalid time string")


def calculate_time(func=None, return_as_last_value=False):
    """Calculate time decorator.

    Apply for your functions to calculate the work time of it.

    Args:
        func:
        return_as_last_value: if True will return (func return value, calc_time).

    Returns:
        prints calc time or returns (func return value, calc_time).
    """
    if func is None:
        return partial(calculate_time, return_as_last_value=return_as_last_value)

    @wraps(func)
    def inner1(*args, **kwargs):
        # storing time before function execution
        begin = time_.time()

        v = func(*args, **kwargs)

        calc_time = time_.time() - begin
        if return_as_last_value:
            return v, calc_time
        else:
            print("Total time taken in : ", func.__name__, calc_time)
            return v

    return inner1
