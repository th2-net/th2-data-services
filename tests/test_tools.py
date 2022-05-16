from th2_data_services.tools import tools
from datetime import datetime
import pytest
from collections import namedtuple

TestCase = namedtuple("TestCase", ["datetime_string", "expected_datetime", "expected_ns", "expected_us"])


@pytest.fixture(params=["nanoseconds", "ns"])
def format_ns(request):
    return request.param


@pytest.fixture(params=["microseconds", "us"])
def format_us(request):
    return request.param


# For 2022-03-05T23:56:44
nanoseconds = 1646513804_000_000_000
microseconds = 1646513804_000_000


@pytest.fixture(params=[
    TestCase("2022-03-05T23:56:44.0Z",
             expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44),
             expected_ns=nanoseconds,
             expected_us=microseconds),
    TestCase("2022-03-05T23:56:44Z",
             expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44),
             expected_ns=nanoseconds,
             expected_us=microseconds),
    TestCase("2022-03-05T23:56:44.123456Z",
             expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456),
             expected_ns=nanoseconds + 123_456_000,
             expected_us=microseconds + 123_456),
    TestCase("2022-03-05T23:56:44.123456789Z",
             expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123456),
             expected_ns=nanoseconds + 123_456_789,
             expected_us=microseconds + 123_456),
    TestCase("2022-03-05T23:56:44.123Z",
             expected_datetime=datetime(year=2022, month=3, day=5, hour=23, minute=56, second=44, microsecond=123),
             expected_ns=nanoseconds + 123_000_000,
             expected_us=microseconds + 123_000),
])
def datetime_strings(request) -> TestCase:
    return request.param


def test_get_time_obj_from_string_ns(datetime_strings, format_ns):
    assert tools.get_time_obj_from_string(datetime_strings.datetime_string, format_ns) == datetime_strings.expected_ns


def test_get_time_obj_from_string_us(datetime_strings, format_us):
    assert tools.get_time_obj_from_string(datetime_strings.datetime_string, format_us) == datetime_strings.expected_us


def test_get_time_obj_from_string_datatime(datetime_strings):
    assert tools.get_time_obj_from_string(datetime_strings.datetime_string,
                                          "datetime") == datetime_strings.expected_datetime


@pytest.mark.parametrize(
    "input_obj",
    [
        ("2022-03-05 23:56:44.233856", "datetime"),
        ("2022-03-05 23:56:44.233856", "microseconds"),
        ("2022-03-05 23:56:44.233856", "nanoseconds"),
        ("2022-03-05T23:56:44.233856Z", "milliseconds"),
    ],
)
def test_get_time_obj_from_string_raises(input_obj):
    with pytest.raises(ValueError):
        tools.get_time_obj_from_string(*input_obj)


@pytest.mark.parametrize(
    "input_obj, expected",
    [
        (({"nano": 1, "epochSecond": 1}, "datetime"), datetime.fromtimestamp(1.000000001)),
        (({"nano": 1, "epochSecond": 1}, "microseconds"), 1000000),
        (({"nano": 1, "epochSecond": 1}, "nanoseconds"), 1000000001),
        (({"nano": 0, "epochSecond": 0}, "datetime"), datetime.fromtimestamp(0.000000000)),
        (({"nano": 0, "epochSecond": 0}, "microseconds"), 0),
        (({"nano": 0, "epochSecond": 0}, "nanoseconds"), 0),
        (({"nano": 999999999, "epochSecond": 1}, "datetime"), datetime.fromtimestamp(1.999999999)),
        (({"nano": 999999999, "epochSecond": 1}, "microseconds"), 1999999),
        (({"nano": 999999999, "epochSecond": 1}, "nanoseconds"), 1999999999),
    ],
)
def test_get_time_obj_from_timestamp(input_obj, expected):
    assert tools.get_time_obj_from_timestamp(*input_obj) == expected


@pytest.mark.parametrize(
    "input_obj",
    [
        ({"nano": 47700.000, "epochSecond": 1634223323}, "datetime"),
        ({"nano": 47700000, "epochSecond": 16342.23323}, "datetime"),
        ({"nano": 0, "epochSecond": 0}, "milliseconds"),
    ],
)
def test_get_time_obj_from_timestamp_raises(input_obj):
    with pytest.raises(ValueError):
        tools.get_time_obj_from_timestamp(*input_obj)
