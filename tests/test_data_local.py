from th2_data_services.data import Data


def test_iter_data(demo_events_from_data_source: Data):
    """Test via data provider"""
    events = demo_events_from_data_source

    # Check that list func works
    assert list(events)

    # Check that we can use Data several times
    assert list(events)


def test_len_data(demo_events_from_data_source: Data):
    events = demo_events_from_data_source

    assert len(events) == 49


def test_filter_data(demo_events_from_data_source: Data):
    events = demo_events_from_data_source
    data = events.filter(lambda r: r["successful"] is False)

    assert len(data) == 6
