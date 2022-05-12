from datetime import datetime


def get_time_obj_from_string(datetime_string: str, format: str = "nanoseconds") -> (datetime, int):
    """Parse datetime object from a string to different format.

    Args:
        datetime_string: Source datetime string to convert.
        format: Transform parameter.
            Values: 'nanoseconds', 'microseconds', 'datetime'. Defaults to 'nanoseconds'.

    Returns:
        obj: Converted object.
    """
    try:
        timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    if format == "nanoseconds":
        return int(timestamp.timestamp() * 10 ** 6) * 1000
    elif format == "microseconds":
        return int(timestamp.timestamp() * 10 ** 6)
    elif format == "datetime":
        return timestamp
    else:
        raise ValueError(f"Format does not support the value: '{format}'")


def get_time_obj_from_timestamp(timestamp: dict, format: str = "nanoseconds") -> (datetime, int):
    """Transform Th2 timestamp to different format.

    Args:
        timestamp:  Th2 timestamp format.
        format: Transform parameter.
            Values: 'nanoseconds', 'microseconds', 'datetime'. Defaults to 'nanoseconds'.

    Returns:
        obj: Converted object.
    """
    datetime_string = f"{timestamp['epochSecond']}{timestamp['nano']:0>9}"
    if format == "nanoseconds":
        return int(datetime_string)
    elif format == "microseconds":
        return int(datetime_string[:-3])
    elif format == "datetime":
        return datetime.fromtimestamp(float(f"{timestamp['epochSecond']}.{timestamp['nano']:0>9}"))
    else:
        raise ValueError(f"Format does not support the value: '{format}'")
