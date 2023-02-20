from datetime import datetime
from typing import Dict, Union


def extract_timestamp(timestamp_element: Dict) -> str:
    """Extracts timestamp from argument.

    Args:
        timestamp_element:

    Returns:
        str
    """
    timestamp = datetime.fromtimestamp(timestamp_element["epochSecond"])
    return f"{timestamp.isoformat()}.{str(timestamp_element['nano']).zfill(9)}"


def time_interval_filter_seconds_precision(
    timestamp_element: Dict, start_timestamp: Union[int, float], end_timestamp: Union[int, float]
) -> bool:
    """TODO: Add Description.

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


def time_slice_object_filter(timestamp_field: Dict, timestamp_iso: str, duration_seconds: int):  # noqa
    # TODO: Add docstings
    ts1 = datetime.fromisoformat(timestamp_iso).timestamp()
    ts2 = ts1 + duration_seconds

    return lambda obj: time_interval_filter_seconds_precision(obj[timestamp_field], ts1, ts2)


def timestamp_aggregation_key(
    global_anchor_timestamp: int, timestamp: int, aggregation_level: str = "seconds"
) -> int:  # noqa
    # TODO: Add docstings
    if aggregation_level == "seconds":
        return timestamp

    aggregation_levels = {
        "minutes": 60,
        "30min": 1800,
        "hours": 3600,
        "1min": 60,
        "5min": 300,
        "10sec": 10,
        "30sec": 30,
    }
    try:
        interval = aggregation_levels[aggregation_level]
    except KeyError:
        raise KeyError(f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}")

    return global_anchor_timestamp + interval * ((timestamp - global_anchor_timestamp) // interval)
