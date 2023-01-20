from collections import namedtuple
from datetime import datetime, timezone

from th2_data_services.interfaces.utils.converter import ITimestampConverter

_DatetimeTuple = namedtuple("DatetimeTuple", "datetime mantissa")


class DatetimeStringConverter(ITimestampConverter[str]):
    """Converts datetime strings.

    If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding).

    Expected timestamp format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z".
    If you don't provide 'Z' in the end, it can return wrong results.
    """

    @classmethod
    def parse_timestamp(cls, datetime_string: str) -> (str, str):
        # Exception handling works faster than using `if`.
        try:
            # Handles "yyyy-MM-ddTHH:mm:ss.SSSSSSSSSZ"
            dt_tuple = _DatetimeTuple(*datetime_string.rsplit("."))
            timestamp = datetime.strptime(dt_tuple.datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        except TypeError:
            # Handles "yyyy-MM-ddTHH:mm:ssZ"
            timestamp = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            dt_tuple = _DatetimeTuple("", "")  # ('2022-03-05T23:56:44', '0Z')

        mantissa_wo_z = dt_tuple.mantissa[:-1]
        nanoseconds = f"{mantissa_wo_z:0<9}"
        seconds = str(int(timestamp.timestamp()))

        return seconds, nanoseconds


class DatetimeConverter(ITimestampConverter[datetime]):
    """Converts datetime objects to timestamp.

    If you request milliseconds but your timestamp has microseconds, they will be just cut (not rounding).
    If you request nanoseconds, last 3 number will be zeros, because datatime object doesn't have nanoseconds.

    Expected timestamp format "datetime.datetime object".
    Expected that you provide UTC time in your data object.
    """

    @classmethod
    def parse_timestamp(cls, datetime_obj: datetime) -> (str, str):
        sec_and_mantissa = str(datetime_obj.replace(tzinfo=timezone.utc).timestamp()).split(".")
        seconds = sec_and_mantissa[0]
        nanoseconds = f"{sec_and_mantissa[1]:0<9}"
        return seconds, nanoseconds


class ProtobufTimestampConverter(ITimestampConverter[dict]):
    """Converts Th2 timestamps.

    If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding).

    Expected timestamp format {'epochSecond': 123, 'nano': 500}.
    """

    @classmethod
    def parse_timestamp(cls, timestamp: dict) -> (str, str):
        seconds, nanoseconds = timestamp["epochSecond"], f"{timestamp['nano']:0>9}"
        return seconds, nanoseconds
