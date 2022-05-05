from th2_data_services.tools import tools
from datetime import datetime


def test_get_time_obj_from_string():
    dt = datetime.fromisoformat("2022-03-05 23:56:44.233856")
    assert (
        tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "datetime") == dt,
        int(dt.timestamp() * 10 ** 6 * 1000) == tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z"),
        int(dt.timestamp() * 10 ** 6) == tools.get_time_obj_from_string("2022-03-05T23:56:44.233856Z", "microseconds"),
    )


def test_get_time_obj_from_timestamp():
    d = {"nano": 477000000, "epochSecond": 1634223323}
    dt = datetime.fromtimestamp(1634223323.477000000)
    assert (
        tools.get_time_obj_from_timestamp(d, "datetime") == dt,
        tools.get_time_obj_from_timestamp(d, "microseconds") == int(dt.timestamp() * 10 ** 6),
        tools.get_time_obj_from_timestamp(d) == int(dt.timestamp() * 10 ** 6 * 1000),
    )
