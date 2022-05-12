from th2_data_services.tools import tools
from datetime import datetime
import pytest


@pytest.mark.parametrize(
    "input_obj, expected",
    [
        (("2022-03-05T23:56:44.233856Z", "datetime"), datetime.fromisoformat("2022-03-05 23:56:44.233856")),
        (
            ("2022-03-05T23:56:44.233856Z", "nanoseconds"),
            datetime.fromisoformat("2022-03-05 23:56:44.233856").timestamp() * 10 ** 9,
        ),
        (
            ("2022-03-05T23:56:44.233856Z", "microseconds"),
            datetime.fromisoformat("2022-03-05 23:56:44.233856").timestamp() * 10 ** 6,
        ),
        (("2022-03-05T23:56:44.0Z", "datetime"), datetime.fromisoformat("2022-03-05 23:56:44")),
        (
            ("2022-03-05T23:56:44.0Z", "microseconds"),
            datetime.fromisoformat("2022-03-05 23:56:44").timestamp() * 10 ** 6,
        ),
        (
            ("2022-03-05T23:56:44.0Z", "nanoseconds"),
            datetime.fromisoformat("2022-03-05 23:56:44").timestamp() * 10 ** 9,
        ),
        (("2022-03-05T23:56:44Z", "datetime"), datetime.fromisoformat("2022-03-05 23:56:44")),
        (("2022-03-05T23:56:44Z", "microseconds"), datetime.fromisoformat("2022-03-05 23:56:44").timestamp() * 10 ** 6),
        (("2022-03-05T23:56:44Z", "nanoseconds"), datetime.fromisoformat("2022-03-05 23:56:44").timestamp() * 10 ** 9),
    ],
)
def test_get_time_obj_from_string(input_obj, expected):
    assert tools.get_time_obj_from_string(*input_obj) == expected


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
