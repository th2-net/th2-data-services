from datetime import datetime

from th2_data_services.data_source import DataSource
from th2_data_services.events_tree import EventsTree
from th2_data_services.data import Data


def test_recover_events_tree(demo_data_source: DataSource):
    start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
    end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)

    events = demo_data_source.get_events_from_data_provider(
        startTimestamp=start_time,
        endTimestamp=end_time,
        metadataOnly=False,
    )

    events_tree = EventsTree(events)

    before_recover_unknown_events = len(events_tree.unknown_events)
    # 2 Missed events
    events_tree.recover_unknown_events(demo_data_source)
    after_recover_unknown_events = len(events_tree.unknown_events)

    assert before_recover_unknown_events != after_recover_unknown_events and after_recover_unknown_events == 0


def test_preserve_body_is_notset(demo_data_source: DataSource):
    start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
    end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)

    events = demo_data_source.get_events_from_data_provider(
        startTimestamp=start_time,
        endTimestamp=end_time,
        metadataOnly=False,
    )

    events_tree = EventsTree(events)
    events_tree.recover_unknown_events(demo_data_source)

    with_body = set()
    for v in events_tree.events.values():
        if v.get("body") is not None:
            with_body.add(True)
        else:
            with_body.add(False)

    assert False in with_body and len(with_body) is 1


def test_preserve_body_is_false(demo_data_source: DataSource):
    start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
    end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)

    events = demo_data_source.get_events_from_data_provider(
        startTimestamp=start_time,
        endTimestamp=end_time,
        metadataOnly=False,
    )

    events_tree = EventsTree(events, preserve_body=False)
    events_tree.recover_unknown_events(demo_data_source)

    with_body = set()
    for v in events_tree.events.values():
        if v.get("body") is not None:
            with_body.add(True)
        else:
            with_body.add(False)

    assert False in with_body and len(with_body) is 1


def test_preserve_body_is_true_recover(demo_data_source: DataSource):
    start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
    end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)

    events = demo_data_source.get_events_from_data_provider(
        startTimestamp=start_time,
        endTimestamp=end_time,
        metadataOnly=False,
    )

    events_tree = EventsTree(events, preserve_body=True)
    events_tree.recover_unknown_events(demo_data_source)

    with_body = set()
    for v in events_tree.events.values():
        if v.get("body") is not None:
            with_body.add(True)
        else:
            with_body.add(False)

    assert True in with_body and len(with_body) is 1
