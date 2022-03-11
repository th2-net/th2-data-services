# def test_recover_events_tree(demo_data_source: DataSource):
#     demo_data_source
# def test_recover_events_tree(demo_data_source: DataSource):
#     start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
#     end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)
#
#     events = demo_data_source.get_events_from_data_provider(
#         startTimestamp=start_time,
#         endTimestamp=end_time,
#         metadataOnly=False,
#     )
#
#     events_tree = EventsTree(events)
#
#     before_recover_unknown_events = len(events_tree.unknown_events)
#     # 2 Missed events
#     events_tree.recover_unknown_events(demo_data_source)
#     after_recover_unknown_events = len(events_tree.unknown_events)
#
#     assert before_recover_unknown_events != after_recover_unknown_events and after_recover_unknown_events == 0
#
#
# def test_recover_unknown_events_with_stub_events(demo_data_source: DataSource):
#     start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
#     end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)
#
#     events = demo_data_source.get_events_from_data_provider(
#         startTimestamp=start_time,
#         endTimestamp=end_time,
#         metadataOnly=False,
#     )
#
#     events = [event for event in events] + [
#         {
#             "attachedMessageIds": [],
#             "batchId": "Broken_Event",
#             "endTimestamp": {"nano": 0, "epochSecond": 0},
#             "startTimestamp": {"nano": 0, "epochSecond": 0},
#             "type": "event",
#             "eventId": f"33499-333-111-test-03221",
#             "eventName": "Broken_Event",
#             "eventType": "Broken_Event",
#             "parentEventId": "Broken_Event",
#             "successful": None,
#             "isBatched": None,
#         }
#     ]
#     events_tree = EventsTree(events)
#     events_tree.recover_unknown_events(demo_data_source, broken_events=True)
#
#     assert (
#         "Broken_Event" not in events_tree.events
#         and events_tree.get_ancestor_by_name({"parentEventId": "33499-333-111-test-03221"}, "Test") is None
#     )
#
#
# def test_preserve_body_is_notset(demo_data_source: DataSource):
#     start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
#     end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)
#
#     events = demo_data_source.get_events_from_data_provider(
#         startTimestamp=start_time,
#         endTimestamp=end_time,
#         metadataOnly=False,
#     )
#
#     events_tree = EventsTree(events)
#     events_tree.recover_unknown_events(demo_data_source)
#
#     with_body = False
#     for v in events_tree.events.values():
#         if v.get("body") is not None:
#             with_body = True
#             break
#
#     assert with_body is False
#
#
# def test_preserve_body_is_false(demo_data_source: DataSource):
#     start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
#     end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)
#
#     events = demo_data_source.get_events_from_data_provider(
#         startTimestamp=start_time,
#         endTimestamp=end_time,
#         metadataOnly=False,
#     )
#
#     events_tree = EventsTree(events, preserve_body=False)
#     events_tree.recover_unknown_events(demo_data_source)
#
#     with_body = False
#     for v in events_tree.events.values():
#         if v.get("body") is not None:
#             with_body = True
#             break
#
#     assert with_body is False
#
#
# def test_preserve_body_is_true_recover(demo_data_source: DataSource):
#     start_time = datetime(year=2021, month=6, day=15, hour=9, minute=45, second=20, microsecond=692724)
#     end_time = datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579)
#
#     events = demo_data_source.get_events_from_data_provider(
#         startTimestamp=start_time,
#         endTimestamp=end_time,
#         metadataOnly=False,
#     )
#
#     events_tree = EventsTree(events, preserve_body=True)
#     events_tree.recover_unknown_events(demo_data_source)
#
#     with_body = True
#     for v in events_tree.events.values():
#         if v.get("body") is None:
#             with_body = False
#             break
#
#     assert with_body is True
