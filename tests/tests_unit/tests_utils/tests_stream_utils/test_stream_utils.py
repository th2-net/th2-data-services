from th2_data_services.data import Data
from th2_data_services.utils.stream_utils.stream_utils import is_sorted


def test_stream_is_sorted_empty():
    assert is_sorted([], lambda e: e["timestamp"]["epochSecond"])


def test_stream_is_sorted_sorted():
    data = Data(
        [
            {"timestamp": {"epochSecond": 1632400658, "nano": 4000000}},
            {"timestamp": {"epochSecond": 1632400658, "nano": 4000023}},
            {"timestamp": {"epochSecond": 1632400659, "nano": 4000000}},
            {"timestamp": {"epochSecond": 1632400670, "nano": 4000000}},
            {"timestamp": {"epochSecond": 1632400689, "nano": 4000000}},
        ]
    )
    result = is_sorted(data, lambda e: e["timestamp"]["epochSecond"])
    assert result and result.get_first_unsorted() is None


def test_stream_is_sorted_not_sorted():
    data = Data(
        [
            {"timestamp": {"epochSecond": 1632400658, "nano": 4000000}},
            {"timestamp": {"epochSecond": 1632400656, "nano": 3000023}},
            {"timestamp": {"epochSecond": 1632400659, "nano": 4000000}},
            {"timestamp": {"epochSecond": 1632400670, "nano": 4000000}},
            {"timestamp": {"epochSecond": 1632400689, "nano": 4000000}},
        ]
    )
    result = is_sorted(data, lambda e: e["timestamp"]["epochSecond"])
    assert not result and result.get_first_unsorted() == 1
