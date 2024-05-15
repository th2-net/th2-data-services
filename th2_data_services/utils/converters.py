#  Copyright 2022-2024 Exactpro (Exactpro Systems Limited)
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

import base64
from datetime import datetime, timezone
import shutil
import gzip
import ciso8601

import flatdict as _flatdict

from th2_data_services.interfaces.utils.converter import ITimestampConverter, TimestampType


class DatetimeStringConverter(ITimestampConverter[str]):
    """Converts datetime strings.

    Works with ISO_8601 datetime strings.

    If you request microseconds but your timestamp has nanoseconds,
    they will be just cut (not rounding).

    Expected timestamp format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS][Z]".
    'Z' in the end is optional.
    """

    @classmethod
    def parse_timestamp(cls, datetime_string: str) -> (str, str):
        # Note:
        #   we have similar code here (not the separate function)
        #   to improve performance.
        try:
            if datetime_string[19] == ".":
                datetime_part, mantissa = datetime_string.rsplit(".")
                if mantissa[-1] == "Z":
                    mantissa = mantissa[:-1]
            else:
                datetime_part, mantissa = datetime_string, ""
        except:
            datetime_part, mantissa = datetime_string, ""

        dt = ciso8601.parse_datetime(datetime_part).replace(tzinfo=timezone.utc)

        nanoseconds = f"{mantissa:0<9}"  # Add zeros on right.
        seconds = str(int(dt.timestamp()))

        return seconds, nanoseconds

    @classmethod
    def parse_timestamp_int(cls, datetime_string: str) -> (int, int):
        # Note:
        #   we have similar code here (not the separate function)
        #   to improve performance.
        try:
            if datetime_string[19] == ".":
                datetime_part, mantissa = datetime_string.rsplit(".")
                if mantissa[-1] == "Z":
                    mantissa = mantissa[:-1]
            else:
                datetime_part, mantissa = datetime_string, ""
        except:
            datetime_part, mantissa = datetime_string, ""

        dt = ciso8601.parse_datetime_as_naive(datetime_part).replace(tzinfo=timezone.utc)

        return int(dt.timestamp()), int(f"{mantissa:0<9}")

    @classmethod
    def to_datetime(cls, datetime_string: str) -> datetime:
        return ciso8601.parse_datetime_as_naive(datetime_string)


class UniversalDatetimeStringConverter(ITimestampConverter[str]):
    """Converts datetime strings.

    If you request microseconds but your timestamp has nanoseconds,
    they will be just cut (not rounding).

    Expected timestamp format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z" or without Z or T as separators.
    """

    @classmethod
    def parse_timestamp(cls, datetime_string: str) -> (str, str):
        try:
            datetime_string = datetime_string.replace("T", " ")
            if datetime_string[19] == ".":
                datetime_part, mantissa = datetime_string.rsplit(".")
                if mantissa[-1] == "Z":
                    mantissa = mantissa[:-1]
            else:
                datetime_part, mantissa = datetime_string, ""
        except:
            datetime_part, mantissa = datetime_string, ""

        dt = ciso8601.parse_datetime(datetime_part).replace(tzinfo=timezone.utc)

        nanoseconds = f"{mantissa:0<9}"  # Add zeros on right.
        seconds = str(int(dt.timestamp()))

        return seconds, nanoseconds

    @classmethod
    def parse_timestamp_int(cls, datetime_string: str) -> (int, int):
        # Note:
        #   we have similar code here (not the separate function)
        #   to improve performance.
        try:
            datetime_string = datetime_string.replace("T", " ")
            if datetime_string[19] == ".":
                datetime_part, mantissa = datetime_string.rsplit(".")
                if mantissa[-1] == "Z":
                    mantissa = mantissa[:-1]
            else:
                datetime_part, mantissa = datetime_string, ""
        except:
            datetime_part, mantissa = datetime_string, ""

        dt = ciso8601.parse_datetime(datetime_part).replace(tzinfo=timezone.utc)

        return int(dt.timestamp()), int(f"{mantissa:0<9}")

    @classmethod
    def to_datetime(cls, datetime_string: str) -> datetime:
        return ciso8601.parse_datetime_as_naive(datetime_string)


class DatetimeConverter(ITimestampConverter[datetime]):
    """Converts datetime objects to timestamp.

    If you request milliseconds but your timestamp has microseconds, they will
    be just cut (not rounding).
    If you request nanoseconds, last 3 number will be zeros, because datatime
    object doesn't have nanoseconds.

    Expected timestamp format "datetime.datetime object".
    Expected that you provide UTC time in your data object.
    """

    @classmethod
    def parse_timestamp(cls, datetime_obj: datetime) -> (str, str):
        sec_and_mantissa = str(datetime_obj.replace(tzinfo=timezone.utc).timestamp()).split(".")
        seconds = sec_and_mantissa[0]
        nanoseconds = f"{sec_and_mantissa[1]:0<9}"  # Add zeros on right.
        return seconds, nanoseconds

    @classmethod
    def parse_timestamp_int(cls, datetime_obj: datetime) -> (int, int):
        # TODO - there should be better solution
        seconds, nanoseconds = cls.parse_timestamp(datetime_obj)
        return int(seconds), int(nanoseconds)


class UnixTimestampConverter(ITimestampConverter[int]):
    """Converts unix timestamp integers to timestamp.

    If you request microseconds but your timestamp has nanoseconds,
    they will be just cut (not rounding).

    Expected timestamp format 1705581844 (seconds), 1705581844123 (milliseconds), 17055818441123456 (microseconds), 17055818441123456789 (nanoseconds).
    Timestamp should be given as integer.
    """

    @classmethod
    def parse_timestamp(cls, unix_timestamp: int) -> (str, str):
        if unix_timestamp < 99999999999:
            return str(unix_timestamp), "000000000"
        elif unix_timestamp < 99999999999999:
            return str(unix_timestamp)[:-3], f"{str(unix_timestamp)[-3:]}000000"
        elif unix_timestamp < 99999999999999999:
            return str(unix_timestamp)[:-6], f"{str(unix_timestamp)[-6:]}000"
        else:
            return str(unix_timestamp)[:-9], str(unix_timestamp)[-9:]

    @classmethod
    def parse_timestamp_int(cls, unix_timestamp: int) -> (int, int):
        seconds, nanoseconds = cls.parse_timestamp(unix_timestamp)
        return int(seconds), int(nanoseconds)


class ProtobufTimestampConverter(ITimestampConverter[dict]):
    """Converts Th2 timestamps.

    If you request microseconds but your timestamp has nanoseconds,
    they will be just cut (not rounding).

    Expected timestamp format {'epochSecond': 123, 'nano': 500}.
    Values are Int.
    """

    @classmethod
    def parse_timestamp(cls, timestamp: dict) -> (str, str):
        seconds, nanoseconds = timestamp["epochSecond"], timestamp["nano"]
        return str(seconds), str(nanoseconds).zfill(9)  # Add zeros on left.

    @classmethod
    def parse_timestamp_int(cls, timestamp: dict) -> (int, int):
        seconds, nanoseconds = timestamp["epochSecond"], timestamp["nano"]
        return seconds, nanoseconds

    @classmethod
    def to_seconds(cls, timestamp: TimestampType):
        """Converts timestamp to seconds.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in seconds format.
        """
        return timestamp["epochSecond"]

    @classmethod
    def to_microseconds(cls, timestamp: TimestampType) -> int:
        """Converts timestamp to microseconds.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in microseconds format.
        """
        seconds, nanoseconds = timestamp["epochSecond"], timestamp["nano"]
        return 1_000_000 * seconds + nanoseconds // 1_000

    @classmethod
    def to_milliseconds(cls, timestamp: TimestampType) -> int:
        """Converts timestamp to milliseconds.

        If your timestamp has nanoseconds, they will be just cut (not rounding).

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in microseconds format.
        """
        seconds, nanoseconds = timestamp["epochSecond"], timestamp["nano"]
        return 1_000 * seconds + nanoseconds // 1_000_000

    @classmethod
    def to_nanoseconds(cls, timestamp: TimestampType) -> int:
        """Converts timestamp to nanoseconds.

        Args:
            timestamp: TimestampType object to convert.

        Returns:
            int: Timestamp in nanoseconds format.
        """
        seconds, nanoseconds = timestamp["epochSecond"], timestamp["nano"]
        return 1_000_000_000 * seconds + nanoseconds


Th2TimestampConverter = ProtobufTimestampConverter


def decompress_gzip_file(input_filename: str, output_filename: str) -> None:
    """Unzip gzip file.

    The original file won't be removed.

    Args:
        input_filename: gzip file path.
        output_filename: out file path.
    """
    with gzip.open(input_filename, "rb") as f_in:
        with open(output_filename, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def flatten_dict(dictionary: dict, separator: str = ".") -> dict:
    """Returns flatten dict.

    Examples:
        >>> rv = flatten_dict({
            'd': [
                {'a': 1,
                 'c': {'z': 2,
                       'b': [{'x': 5, 'y': 10}, 'str-in-lst']
                       }
                 },
                'str',
                3
            ]
        }
        )

        assert rv == {
            'd.0.a': 1,
            'd.0.c.z': 2,
            'd.0.c.b.0.x': 5,
            'd.0.c.b.0.y': 10,
            'd.0.c.b.1': 'str-in-lst',
            'd.1': 'str',
            'd.2': 3
        }

    Args:
        dictionary: dict object.
        parent_key: used for internal function purposes.
        separator: the separator between words.

    Returns:
        Flatten dict.

    """
    rv = _flatdict.FlatterDict(dictionary, delimiter=separator)
    return dict(rv)


def decode_base64(coded_string: str) -> bytes:
    """Returns decoded bytes."""
    return base64.b64decode(coded_string)
