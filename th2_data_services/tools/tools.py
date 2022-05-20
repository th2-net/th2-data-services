from datetime import datetime, timezone


def get_time_obj_from_string(datetime_string: str, format: str = "nanoseconds") -> (datetime, int):
    """Convert datetime string to different format.

    Args:
        datetime_string: Source datetime string to convert. Expected format "yyyy-MM-ddTHH:mm:ss.[SSSSSSSSS]Z"
        format: Transform parameter. Defaults to 'nanoseconds'.
            Possible values:
            - 'nanoseconds' or 'ns'
            - 'microseconds' or 'us'
            - 'datetime'

    Returns:
        obj: Converted object.
    """
    ds = ("", "")
    try:
        timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        ds = datetime_string.rsplit(".")
        timestamp = datetime.strptime(ds[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    sec = f"{ds[1][:-1]}{'0' * (9 - len(ds[1][:-1]))}"
    timestamp = int(timestamp.timestamp())
    if format == "nanoseconds" or format == "ns":
        return int(f"{timestamp}{sec}")
    elif format == "microseconds" or format == "us":
        return int(f"{timestamp}{sec[:-3]}")
    elif format == "datetime":
        sec = sec[:-3]
        sec = str(int(sec[::-1]))[::-1]
        return datetime.utcfromtimestamp(float(f"{timestamp}")).replace(tzinfo=timezone.utc, microsecond=int(sec))
    else:
        raise ValueError(f"Format does not support the value: '{format}'")


def get_time_obj_from_timestamp(timestamp: dict, format: str = "nanoseconds") -> (datetime, int):
    """Transform Th2 timestamp to different format.

    Args:
        timestamp: Th2 timestamp format.
        format: Transform parameter.
            Values: 'nanoseconds', 'microseconds', 'datetime'. Defaults to 'nanoseconds'.

    Returns:
        obj: Converted object.
    """
    datetime_string = f"{timestamp['epochSecond']}{timestamp['nano']:0>9}"
    if format == "nanoseconds" or format == "ns":
        return int(datetime_string)
    elif format == "microseconds" or format == "us":
        return int(datetime_string[:-3])
    elif format == "datetime":
        return datetime.utcfromtimestamp(float(f"{timestamp['epochSecond']}.{timestamp['nano']:0>9}"))
    else:
        raise ValueError(f"Format does not support the value: '{format}'")
