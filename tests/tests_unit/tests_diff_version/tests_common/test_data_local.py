import pytest

from th2_data_services.data import Data


@pytest.mark.skip
def test_iter_data(demo_events_from_data_source: Data):
    """Test via data provider"""
    # output = [
    #     {"eventName": "test1", "eventId": "id1"},
    #     {"eventName": "test2", "eventId": "id2"},
    #     {"eventName": "test3", "eventId": "id3"},
    # ]
    # mocker.patch("", )
    # TODO: Change on mock
    events = demo_events_from_data_source

    # Check that list func works
    assert list(events)

    # Check that we can use Data several times
    assert list(events)


def test_filter_data(demo_events_from_data_source: Data):
    # TODO: Change on mock
    events = demo_events_from_data_source
    data = events.filter(lambda r: r["successful"] is False)

    assert len(list(data)) == 23
