from th2_data_services.tools import tools
from datetime import datetime
import pytest


def test_get_time_obj_from_string():
    dt = datetime.fromisoformat("2022-03-05 23:56:44.233856")
    dt_1 = datetime.fromisoformat("2022-03-05 23:56:44")
    assert all(
        [
            tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "datetime") == dt,
            int(dt.timestamp() * 10 ** 6) * 1000 == tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z"),
            int(dt.timestamp() * 10 ** 6)
            == tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "microseconds"),
            tools.get_time_obj_from_string("2022-03-05T23:56:44.0Z", "datetime") == dt_1,
            int(dt_1.timestamp() * 10 ** 6) * 1000 == tools.get_time_obj_from_string("2022-03-05T23:56:44.0Z"),
            int(dt_1.timestamp() * 10 ** 6) == tools.get_time_obj_from_string("2022-03-05T23:56:44.0Z", "microseconds"),
            tools.get_time_obj_from_string("2022-03-05T23:56:44Z", "datetime") == dt_1,
            int(dt_1.timestamp() * 10 ** 6) * 1000 == tools.get_time_obj_from_string("2022-03-05T23:56:44Z"),
            int(dt_1.timestamp() * 10 ** 6) == tools.get_time_obj_from_string("2022-03-05T23:56:44Z", "microseconds"),
        ]
    )

    with pytest.raises(ValueError):
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856", "datetime")
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856", "microseconds")
        tools.get_time_obj_from_string("2022-03-05 23:56:44.233856")
        tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "milliseconds")


def test_get_time_obj_from_timestamp():
    d = {"nano": 1, "epochSecond": 1}
    dt = datetime.fromtimestamp(1.000000001)
    d_1 = {"nano": 0, "epochSecond": 0}
    dt_1 = datetime.fromtimestamp(0.000000000)
    d_2 = {"nano": 999999999, "epochSecond": 1}
    dt_2 = datetime.fromtimestamp(1.999999999)
    assert all(
        [
            tools.get_time_obj_from_timestamp(d, "datetime") == dt,
            tools.get_time_obj_from_timestamp(d, "microseconds") == 1000000,
            tools.get_time_obj_from_timestamp(d) == 1000000001,
            tools.get_time_obj_from_timestamp(d_1, "datetime") == dt_1,
            tools.get_time_obj_from_timestamp(d_1, "microseconds") == 0,
            tools.get_time_obj_from_timestamp(d_1) == 0,
            tools.get_time_obj_from_timestamp(d_2, "datetime") == dt_2,
            tools.get_time_obj_from_timestamp(d_2, "microseconds") == 1999999,
            tools.get_time_obj_from_timestamp(d_2) == 1999999999,
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
