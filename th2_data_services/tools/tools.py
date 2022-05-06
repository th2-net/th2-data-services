from datetime import datetime


def get_time_obj_from_string(date_string: str, format: str = "nanoseconds") -> (datetime, int):
    """Parse datetime object from a string to different format.

    Args:
        date_string: Source datetime string to convert.
        format: Transform parameter. Default value: 'nanoseconds'.

    Returns:
        obj: Converted object.
    """
    try:
        timestamp = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        timestamp = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    if format == "nanoseconds":
        return int(timestamp.timestamp() * 10 ** 6) * 1000
    elif format == "microseconds":
        return int(timestamp.timestamp() * 10 ** 6)
    elif format == "datetime":
        return timestamp
    else:
        raise ValueError(f"Format does not match argument: '{format}'")


def get_time_obj_from_timestamp(timestamp: dict, format: str = "nanoseconds") -> (datetime, int):
    """Transform Th2 timestamp to different format.

    Args:
        timestamp:  Th2 timestamp format.
        format: Transform parameter. Default value: 'nanoseconds'.

    Returns:
        obj: Converted object.
    """
    _ts = int(f"{timestamp['epochSecond']}{timestamp['nano']:0>9}")
    if format == "nanoseconds":
        return _ts
    elif format == "microseconds":
        return _ts // 10 ** 3
    elif format == "datetime":
        return datetime.fromtimestamp(_ts / 10 ** 9)
    else:
        raise ValueError(f"Format does not match argument: '{format}'")
