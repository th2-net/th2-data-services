from collections import namedtuple
from datetime import datetime, timezone

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


class DatetimeConverter(ITimestampConverter[datetime]):
    """Converts datetime objects to timestamp.

    If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding).

    Expected datetime object shouldn't contain microseconds.
    """

    @classmethod
    def parse_timestamp(cls, datetime_obj: datetime) -> (str, str):
        seconds = str(int(datetime_obj.timestamp()))
        nanoseconds = "0" * 9
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
