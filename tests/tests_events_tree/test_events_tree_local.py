from datetime import datetime

from th2_data_services.data_source import DataSource
from th2_data_services.events_tree import EventsTree


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
