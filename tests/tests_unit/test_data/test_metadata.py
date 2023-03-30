from typing import List

from th2_data_services.data import Data


def test_metadata_is_carried(general_data: List[dict]):
    data = Data(general_data)
    metadata = {"some": "default value", "test": "case"}
    data.update_metadata(metadata)
    data2 = data.filter(lambda event: event["isBatched"]).map(lambda event: {"id": event["eventId"]})
    assert data2.metadata == metadata


def test_updating_one_data_object_metadata_dont_affect_parent_data(general_data: List[dict]):
    data = Data(general_data)
    metadata = {"some": "default value", "test": "case"}
    data.update_metadata(metadata)
    data2 = data.filter(lambda event: event["isBatched"]).map(lambda event: {"id": event["eventId"]})
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
