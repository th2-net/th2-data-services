from collections import namedtuple
from datetime import datetime, timezone

import pytest

from th2_data_services.utils.converters import (
    DatetimeStringConverter,
    DatetimeConverter,
    ProtobufTimestampConverter,
)

TestCase = namedtuple(
    "TestCase",
    [
        "datetime_string",
        "datetime_obj",
        "th2_timestamp",
        "expected_datetime",
        "expected_ns",
        "expected_us",
        "expected_ms",
    ],
)

# For 2022-03-05T23:56:44
nanoseconds = 1646524604_000_000_000
microseconds = 1646524604_000_000
milliseconds = 1646524604_000
seconds = 1646524604


@pytest.fixture(
    params=[
        TestCase(
            datetime_string="2022-03-05T23:56:44.0Z",
            datetime_obj=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44),
            th2_timestamp={"epochSecond": seconds, "nano": 0},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, tzinfo=timezone.utc
            ),
            expected_ns=nanoseconds,
            expected_us=microseconds,
            expected_ms=milliseconds,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44Z",
            datetime_obj=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44),
            th2_timestamp={"epochSecond": seconds, "nano": 0},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, tzinfo=timezone.utc
            ),
            expected_ns=nanoseconds,
            expected_us=microseconds,
            expected_ms=milliseconds,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.123456Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 123_456_000},
            expected_datetime=datetime(
                year=2022,
                month=3,
                day=5,
                hour=23,
                minute=56,
                second=44,
                microsecond=123456,
                tzinfo=timezone.utc,
            ),
            expected_ns=nanoseconds + 123_456_000,
            expected_us=microseconds + 123_456,
            expected_ms=milliseconds + 123,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.123456789Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 123_456_789},
            expected_datetime=datetime(
                year=2022,
                month=3,
                day=5,
                hour=23,
                minute=56,
                second=44,
                microsecond=123456,
                tzinfo=timezone.utc,
            ),
            expected_ns=nanoseconds + 123_456_789,
            expected_us=microseconds + 123_456,
            expected_ms=milliseconds + 123,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.123Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123000
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 123_000_000},
            expected_datetime=datetime(
                year=2022,
                month=3,
                day=5,
                hour=23,
                minute=56,
                second=44,
                microsecond=123000,
                tzinfo=timezone.utc,
            ),
            expected_ns=nanoseconds + 123_000_000,
            expected_us=microseconds + 123_000,
            expected_ms=milliseconds + 123,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.00123Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=1230
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 1_230_000},
            expected_datetime=datetime(
                year=2022,
                month=3,
                day=5,
                hour=23,
                minute=56,
                second=44,
                microsecond=1230,
                tzinfo=timezone.utc,
            ),
            expected_ns=nanoseconds + 1_230_000,
            expected_us=microseconds + 1_230,
            expected_ms=milliseconds + 1,
        ),
    ]
)
def datetime_strings(request) -> TestCase:
    return request.param


@pytest.fixture(
    params=[
        DatetimeStringConverter,
        DatetimeConverter,
        ProtobufTimestampConverter,
    ]
)
def converters(request) -> TestCase:
    return request.param
