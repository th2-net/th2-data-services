from collections import namedtuple
from datetime import datetime

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
        "expected_s",
        "expected_datestring",
        "expected_th2_timestamp",
        "expected_th2_timestamp_datetime",
    ],
)

# For 2022-03-05T23:56:44
nanoseconds = 1646524604_000_000_000
microseconds = 1646524604_000_000
milliseconds = 1646524604_000
seconds = 1646524604


@pytest.fixture(
    params=[
        # 0
        # TestCase(
        #     datetime_string="2022-03-05T23:56:44.0Z",
        #     datetime_obj=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44),
        #     th2_timestamp={"epochSecond": seconds, "nano": 0},
        #     expected_datetime=datetime(
        #         year=2022, month=3, day=5, hour=23, minute=56, second=44
        #     ),
        #     expected_ns=nanoseconds,
        #     expected_us=microseconds,
        #     expected_ms=milliseconds,
        #     expected_datestring='2022-03-05T23:56:44.000000000',
        # ),
        # # 1
        # TestCase(
        #     datetime_string="2022-03-05T23:56:44Z",
        #     datetime_obj=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44),
        #     th2_timestamp={"epochSecond": seconds, "nano": 0},
        #     expected_datetime=datetime(
        #         year=2022, month=3, day=5, hour=23, minute=56, second=44
        #     ),
        #     expected_ns=nanoseconds,
        #     expected_us=microseconds,
        #     expected_ms=milliseconds,
        #     expected_datestring='2022-03-05T23:56:44.000000000',
        # ),
        # # 2
        # TestCase(
        #     datetime_string="2022-03-05T23:56:44.123456Z",
        #     datetime_obj=datetime(
        #         year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456
        #     ),
        #     th2_timestamp={"epochSecond": seconds, "nano": 123_456_000},
        #     expected_datetime=datetime(
        #         year=2022,
        #         month=3,
        #         day=5,
        #         hour=23,
        #         minute=56,
        #         second=44,
        #         microsecond=123456
        #     ),
        #     expected_ns=nanoseconds + 123_456_000,
        #     expected_us=microseconds + 123_456,
        #     expected_ms=milliseconds + 123,
        #     expected_datestring='2022-03-05T23:56:44.123456000',
        # ),
        # 3
        TestCase(
            datetime_string="2022-03-05T23:56:44.123456789Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 123_456_789},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456
            ),
            expected_ns=nanoseconds + 123_456_789,
            expected_us=microseconds + 123_456,
            expected_ms=milliseconds + 123,
            expected_s=seconds,
            # expected_datestring --
            #   DatetimeConverter will have '2022-03-05T23:56:44.123456000'
            expected_datestring="2022-03-05T23:56:44.123456789",
            expected_th2_timestamp={"epochSecond": seconds, "nano": 123_456_789},
            expected_th2_timestamp_datetime={"epochSecond": seconds, "nano": 123_456_000},
        ),
        # 4
        TestCase(
            datetime_string="2022-03-05T23:56:44.123Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123000
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 123_000_000},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123000
            ),
            expected_ns=nanoseconds + 123_000_000,
            expected_us=microseconds + 123_000,
            expected_ms=milliseconds + 123,
            expected_s=seconds,
            expected_datestring="2022-03-05T23:56:44.123000000",
            expected_th2_timestamp={"epochSecond": seconds, "nano": 123_000_000},
            expected_th2_timestamp_datetime={"epochSecond": seconds, "nano": 123_000_000},
        ),
        # 5
        TestCase(
            datetime_string="2022-03-05T23:56:44.00123Z",
            datetime_obj=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=1230
            ),
            th2_timestamp={"epochSecond": seconds, "nano": 1_230_000},
            expected_datetime=datetime(
                year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=1230
            ),
            expected_ns=nanoseconds + 1_230_000,
            expected_us=microseconds + 1_230,
            expected_ms=milliseconds + 1,
            expected_s=seconds,
            expected_datestring="2022-03-05T23:56:44.001230000",
            expected_th2_timestamp={"epochSecond": seconds, "nano": 1_230_000},
            expected_th2_timestamp_datetime={"epochSecond": seconds, "nano": 1_230_000},
        ),
        # 6
        TestCase(
            datetime_string="2024-05-07T05:49:47.742201",
            datetime_obj=datetime(
                year=2024, month=5, day=7, hour=5, minute=49, second=47, microsecond=742201
            ),
            th2_timestamp={"epochSecond": 1715060987, "nano": 742201000},
            expected_datetime=datetime(
                year=2024, month=5, day=7, hour=5, minute=49, second=47, microsecond=742201
            ),
            expected_ns=1715060987742201000,
            expected_us=1715060987742201,
            expected_ms=1715060987742,
            expected_s=1715060987,
            expected_datestring="2024-05-07T05:49:47.742201000",
            expected_th2_timestamp={"epochSecond": 1715060987, "nano": 742201000},
            expected_th2_timestamp_datetime={"epochSecond": 1715060987, "nano": 742201000},
        ),
        # 7
        TestCase(
            datetime_string="2024-05-07T05:49:47Z",
            datetime_obj=datetime(
                year=2024, month=5, day=7, hour=5, minute=49, second=47, microsecond=0
            ),
            th2_timestamp={"epochSecond": 1715060987, "nano": 0},
            expected_datetime=datetime(
                year=2024, month=5, day=7, hour=5, minute=49, second=47, microsecond=0
            ),
            expected_ns=1715060987000000000,
            expected_us=1715060987000000,
            expected_ms=1715060987000,
            expected_s=1715060987,
            expected_datestring="2024-05-07T05:49:47.000000000",
            expected_th2_timestamp={"epochSecond": 1715060987, "nano": 0},
            expected_th2_timestamp_datetime={"epochSecond": 1715060987, "nano": 0},
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
