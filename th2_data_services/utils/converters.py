from collections import namedtuple
from datetime import datetime, timezone
from typing import Union

from th2_data_services.interfaces.utils.converter import ITimestampConverter

_DatetimeTuple = namedtuple("DatetimeTuple", "datetime mantissa")


class DatetimeStringConverter(ITimestampConverter[str]):
    """Converts datetime strings.

    If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding).

    Expected timestamp format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z".
    """

    @classmethod
    def parse_timestamp(cls, datetime_string: str) -> (str, str):
        try:
            dt_tuple = _DatetimeTuple("", "")  # ('2022-03-05T23:56:44', '0Z')
            timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            dt_tuple = _DatetimeTuple(*datetime_string.rsplit("."))
            timestamp = datetime.strptime(dt_tuple.datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)

        mantissa_wo_z = dt_tuple.mantissa[:-1]
        nanoseconds = f"{mantissa_wo_z:0<9}"
        seconds = int(timestamp.timestamp())

        return seconds, nanoseconds


def datetime_string_to_time_obj(datetime_string: str, to: str = "nanoseconds") -> Union[datetime, int]:
    """Convert datetime string to unix timestamp or datetime object.

    If you request microseconds but your datetime string has nanoseconds, they will be just cut (not rounding).

    Args:
        datetime_string: Datetime string to convert. Expected format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z"
        to: Convert parameter. The default value is 'nanoseconds'.
            Possible values:
            - 'nanoseconds' or 'ns'
            - 'microseconds' or 'us'
            - 'datetime'

    Returns:
        obj: Converted object.
    """
    try:
        dt_tuple = _DatetimeTuple("", "")  # ('2022-03-05T23:56:44', '0Z')
        timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        dt_tuple = _DatetimeTuple(*datetime_string.rsplit("."))
        timestamp = datetime.strptime(dt_tuple.datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)

    mantissa_wo_z = dt_tuple.mantissa[:-1]
    nanoseconds = f"{mantissa_wo_z:0<9}"
    seconds = int(timestamp.timestamp())

    if to == "nanoseconds" or to == "ns":
        return int(f"{seconds}{nanoseconds}")
    elif to == "microseconds" or to == "us":
        return int(f"{seconds}{nanoseconds[:-3]}")
    elif to == "datetime":
        microseconds = nanoseconds[:-3]
        microseconds = str(int(microseconds[::-1]))[::-1]  # Convert .123000 microseconds to 123 milliseconds
        return datetime.utcfromtimestamp(seconds).replace(tzinfo=timezone.utc, microsecond=int(microseconds))
    else:
        raise ValueError(f"Unexpected conversion type: '{to}'")


def th2_timestamp_to_time_obj(timestamp: dict, to: str = "nanoseconds") -> Union[datetime, int]:
    """Convert Th2 timestamp to unix timestamp or datetime object.

    If you request microseconds but your datetime string has nanoseconds, they will be just cut (not rounding).

    Args:
        timestamp: Th2 timestamp object to convert.
        to: Transform parameter. The default value is 'nanoseconds'.
            Possible values:
            - 'nanoseconds' or 'ns'
            - 'microseconds' or 'us'
            - 'datetime'

    Returns:
        obj: Converted object.
    """
    unixtime_string_ns = f"{timestamp['epochSecond']}{timestamp['nano']:0>9}"
    if to == "nanoseconds" or to == "ns":
        return int(unixtime_string_ns)
    elif to == "microseconds" or to == "us":
        return int(unixtime_string_ns[:-3])
    elif to == "datetime":
        return datetime.utcfromtimestamp(float(f"{timestamp['epochSecond']}.{timestamp['nano']:0>9}"))
    else:
        raise ValueError(f"Unexpected conversion type: '{to}'")
