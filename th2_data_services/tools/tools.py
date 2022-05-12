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
    ds = ("", "")
    try:
        timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        ds = datetime_string.rsplit(".")
        timestamp = datetime.strptime(ds[0], "%Y-%m-%dT%H:%M:%S")
    sec = f"{ds[1][:-1]}{'0' * (9 - len(ds[1][:-1]))}"
    timestamp = int(timestamp.timestamp())
    if format == "nanoseconds":
        return int(f"{timestamp}{sec}")
    elif format == "microseconds":
        return int(f"{timestamp}{sec[:-3]}")
    elif format == "datetime":
        return datetime.fromtimestamp(float(f"{timestamp}.{sec}"))
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
