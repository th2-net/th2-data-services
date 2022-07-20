from collections import namedtuple
from datetime import datetime, timezone

import pytest


TestCase = namedtuple(
    "TestCase", ["datetime_string", "th2_timestamp", "expected_datetime", "expected_ns", "expected_us"]
)

# For 2022-03-05T23:56:44
nanoseconds = 1646524604_000_000_000
microseconds = 1646524604_000_000
seconds = 1646524604


@pytest.fixture(
    params=[
        TestCase(
            datetime_string="2022-03-05T23:56:44.0Z",
            th2_timestamp={"epochSecond": seconds, "nano": 0},
            expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44, tzinfo=timezone.utc),
            expected_ns=nanoseconds,
            expected_us=microseconds,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44Z",
            th2_timestamp={"epochSecond": seconds, "nano": 0},
            expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44, tzinfo=timezone.utc),
            expected_ns=nanoseconds,
            expected_us=microseconds,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.123456Z",
            th2_timestamp={"epochSecond": seconds, "nano": 123_456_000},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456, tzinfo=timezone.utc
            ),
            expected_ns=nanoseconds + 123_456_000,
            expected_us=microseconds + 123_456,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.123456789Z",
            th2_timestamp={"epochSecond": seconds, "nano": 123_456_789},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456, tzinfo=timezone.utc
            ),
            expected_ns=nanoseconds + 123_456_789,
            expected_us=microseconds + 123_456,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.123Z",
            th2_timestamp={"epochSecond": seconds, "nano": 123_000_000},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123000, tzinfo=timezone.utc
            ),
            expected_ns=nanoseconds + 123_000_000,
            expected_us=microseconds + 123_000,
        ),
        TestCase(
            datetime_string="2022-03-05T23:56:44.00123Z",
            th2_timestamp={"epochSecond": seconds, "nano": 1_230_000},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=1230, tzinfo=timezone.utc
            ),
            expected_ns=nanoseconds + 1_230_000,
            expected_us=microseconds + 1_230,
        ),
    ]
)
def datetime_strings(request) -> TestCase:
    return request.param
