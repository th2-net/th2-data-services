from typing import List

from th2_data_services.data import Data


def test_metadata_is_carried(general_data: List[dict]):
    data = Data(general_data)
    metadata = {"some": "default value", "test": "case"}
    data.update_metadata(metadata)
    data2 = data.filter(lambda event: event["isBatched"]).map(
        lambda event: {"id": event["eventId"]}
    )
    assert data2.metadata == metadata


def test_updating_one_data_object_metadata_dont_affect_parent_data(general_data: List[dict]):
    data = Data(general_data)
    metadata = {"some": "default value", "test": "case"}
    data.update_metadata(metadata)
    data2 = data.filter(lambda event: event["isBatched"]).map(
        lambda event: {"id": event["eventId"]}
    )
    data2.update_metadata({"a": 123})
    assert data.metadata != data2.metadata


def test_metadata_joining_iadd(general_data: List[dict]):
    data = Data(general_data)
    metadata = {"some": "default value", "test": "case"}
    data.update_metadata(metadata)

    data += Data([1, 2, 3])
    assert data.metadata == metadata

    data_m_metadata = {"a": "nums"}
    data_m = Data([4, 5, 6]).update_metadata(data_m_metadata)

    data += data_m
    exp_metadata = metadata.copy()
    exp_metadata.update(data_m_metadata)
    assert data.metadata == exp_metadata


def test_metadata_joining_add(general_data: List[dict]):
    data = Data(general_data)
    metadata = {"some": "default value", "test": "case"}
    data.update_metadata(metadata)

    data1 = data + Data([1, 2, 3])
    assert data1.metadata == metadata

    data_m_metadata = {"a": "nums"}
    data_m = Data([4, 5, 6]).update_metadata(data_m_metadata)

    data2 = data + data_m
    exp_metadata = metadata.copy()
    exp_metadata.update(data_m_metadata)
    assert data2.metadata == exp_metadata


def test_source_file_in_metadata_removed_when_adding():
    data1 = Data([1, 2, 3])
    data2 = Data([4, 5, 6])
    data1.update_metadata({"source_file": "file1"})
    data2.update_metadata({"source_file": "file2"})
    data3 = data1 + data2

    assert data3.metadata["source_files"] == ["file1", "file2"]


def test_strings_update_in_metadata():
    """
    If both values of same key are strings update replaces the value.
    If at least one value is a list, second value is pushed into the list.
    """
    data1 = Data([1, 2, 3])
    data1.update_metadata(
        {"test_str": "str1", "test_list_and_str": ["str1"], "test_list_and_list": ["str1"]}
    )
    data1.update_metadata(
        {"test_str": "str2", "test_list_and_str": "str2", "test_list_and_list": ["str2"]}
    )

    assert data1.metadata == {
        "test_str": "str2",
        "test_list_and_str": ["str1", "str2"],
        "test_list_and_list": ["str1", "str2"],
    }


def test_metadata_update_with_string_as_value_in_dict():
    data = Data([])
    data.update_metadata({1: "ab"})
    data.update_metadata({1: "cd"})

    exp_metadata = {1: "cd"}
    assert data.metadata == exp_metadata


def test_metadata_update_with_change_type_change():
    data = Data([])
    data.update_metadata({1: ["ab"]})
    data.update_metadata({1: "cd"}, change_type="change")

    exp_metadata = {1: "cd"}
    assert data.metadata == exp_metadata
