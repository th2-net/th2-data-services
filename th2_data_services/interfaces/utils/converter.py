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

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar, Tuple

TimestampType = TypeVar("TimestampType")

"""
Some speed tests:
=========================

1) Seconds to UTC datetime conversion

    [1]
        %timeit datetime.fromtimestamp(seconds, tz=timezone.utc)
        329 ns � 1.16 ns per loop (mean � std. dev. of 7 runs, 1,000,000 loops each)
    
    [2]
        %timeit datetime.utcfromtimestamp(seconds).replace(tzinfo=timezone.utc)
        781 ns � 10.8 ns per loop (mean � std. dev. of 7 runs, 1,000,000 loops each)
    
    [3]
        %timeit datetime.utcfromtimestamp(seconds)
        116 ns � 8.47 ns per loop (mean � std. dev. of 7 runs, 10,000,000 loops each)
"""


class ITimestampConverter(ABC, Generic[TimestampType]):
    @classmethod
    @abstractmethod
    def parse_timestamp(cls, timestamp: TimestampType) -> Tuple[str, str]:
        """Returns string representation of Unix time.

        Separated for seconds and nanoseconds.

        Please note, nanoseconds can have zeroes from left.

        e.g. 2022-03-05T23:56:44.00123Z -> ('1646524604', '001230000')
        """

    @classmethod
    @abstractmethod
    def parse_timestamp_int(cls, timestamp: TimestampType) -> Tuple[int, int]:
        """Returns int representation of Unix time.

        Separated for seconds and nanoseconds.

        e.g. 2022-03-05T23:56:44.00123Z -> (1646524604, 001230000)
        """

    @classmethod
    def to_datetime(cls, timestamp: TimestampType) -> datetime:
        """Converts timestamp to UTC datetime object.

        If your timestamp has nanoseconds, they will be just cut (not rounded).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            datetime: Timestamp in python datetime format.
        """
        seconds, nanoseconds = cls.parse_timestamp_int(timestamp)
        return datetime.utcfromtimestamp(seconds + nanoseconds // 1000 / 1_000_000)

    @classmethod
    def to_seconds(cls, timestamp: TimestampType):
        """Converts timestamp to seconds.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in seconds format.
        """
        seconds, nanoseconds = cls.parse_timestamp_int(timestamp)
        return seconds

    @classmethod
    def to_milliseconds(cls, timestamp: TimestampType) -> int:
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
    def to_nanoseconds(cls, timestamp: TimestampType) -> int:
        """Converts timestamp to nanoseconds.

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in nanoseconds format.
        """
        seconds, nanoseconds = cls.parse_timestamp(timestamp)
        return int(f"{seconds}{nanoseconds}")

    @classmethod
    def to_datetime_str(cls, timestamp: TimestampType) -> str:
        """Converts timestamp to UTC datetime string in ISO format.

        Format example:
            - 2022-03-06T04:56:44.123456789
            - 2022-03-06T04:56:44.000000000

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            str: datetime string in YYYY-MM-DDTHH:MM:SS.mmmmmm format.
        """
        seconds, nanoseconds = cls.parse_timestamp(timestamp)
        dt = datetime.utcfromtimestamp(int(seconds))
        return f"{dt.isoformat()}.{nanoseconds}"

    @classmethod
    def to_th2_timestamp(cls, timestamp: TimestampType) -> dict:
        """Converts timestamp to th2 timestamp.

        Args:
            timestamp: int object to convert.

        Returns:
            dict: {"epochSecond": seconds, "nano": nanoseconds}
        """
        seconds, nanoseconds = cls.parse_timestamp_int(timestamp)
        return {"epochSecond": seconds, "nano": nanoseconds}
