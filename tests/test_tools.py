from th2_data_services.tools import tools
from datetime import datetime
import pytest


def test_get_time_obj_from_string():
    dt = datetime.fromisoformat("2022-03-05 23:56:44.233856")
    assert all(
        [
            tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "datetime") == dt,
            int(dt.timestamp() * 10 ** 6) * 1000 == tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z"),
            int(dt.timestamp() * 10 ** 6)
            == tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "microseconds"),
        ]
    )

    with pytest.raises(ValueError):
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856", "datetime")
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856", "microseconds")
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856")
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856", "datetime")
        tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "milliseconds")


def test_get_time_obj_from_timestamp():
    d = {"nano": 477000000, "epochSecond": 1634223323}
    dt = datetime.fromtimestamp(1634223323.477000000)
    assert all(
        [
            tools.get_time_obj_from_timestamp(d, "datetime") == dt,
            tools.get_time_obj_from_timestamp(d, "microseconds") == int(dt.timestamp() * 10 ** 6),
            tools.get_time_obj_from_timestamp(d) == int(dt.timestamp() * 10 ** 6) * 1000,
        ]
    )
    incorrect_d_0 = {"nano": 4770.0000, "epochSecond": 1634223323}
    incorrect_d_1 = {"nano": 47700000, "epochSecond": 16342.23323}
    incorrect_d_2 = {"nan": 47700000, "epochSecond": 1634223323}
    incorrect_d_3 = {"nano": 47700000, "epoch": 1634223323}
    with pytest.raises(ValueError):
        tools.get_time_obj_from_timestamp(incorrect_d_0, "datetime")
        tools.get_time_obj_from_timestamp(incorrect_d_1, "datetime")
        tools.get_time_obj_from_timestamp(incorrect_d_2, "datetime")
        tools.get_time_obj_from_timestamp(incorrect_d_3, "datetime")
        tools.get_time_obj_from_timestamp(d, "milliseconds")
