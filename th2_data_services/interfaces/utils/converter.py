from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Generic, TypeVar

TimestampType = TypeVar("TimestampType")


class ITimestampConverter(ABC, Generic[TimestampType]):
    @classmethod
    @abstractmethod
    def parse_timestamp(cls, timestamp: TimestampType) -> (str, str):
        """Returns string representation of Unix time separated to seconds and nanoseconds.

        e.g. 2022-03-05T23:56:44.00123Z -> ('1646524604', '001230000')
        """

    @classmethod
    def to_datetime(cls, timestamp: TimestampType) -> datetime:
        """Converts timestamp to datetime object.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            datetime: Timestamp in python datetime format.
        """
        seconds, nanoseconds = cls.parse_timestamp(timestamp)
        microseconds = nanoseconds[:-3]
        return datetime.utcfromtimestamp(int(seconds)).replace(tzinfo=timezone.utc, microsecond=int(microseconds))

    @classmethod
    def to_microseconds(cls, timestamp: TimestampType) -> int:
        """Converts timestamp to microseconds.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in microseconds format.
        """
        seconds, nanoseconds = cls.parse_timestamp(timestamp)
        return int(f"{seconds}{nanoseconds[:-3]}")

    @classmethod
    def to_milliseconds(cls, timestamp: TimestampType):
        """Converts timestamp to milliseconds.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in microseconds format.
        """
        seconds, nanoseconds = cls.parse_timestamp(timestamp)
        return int(f"{seconds}{nanoseconds[:-6]}")

    @classmethod
    def to_nanoseconds(cls, timestamp: TimestampType) -> int:
        """Converts timestamp to nanoseconds.

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in nanoseconds format.
        """
        seconds, nanoseconds = cls.parse_timestamp(timestamp)
        return int(f"{seconds}{nanoseconds}")
