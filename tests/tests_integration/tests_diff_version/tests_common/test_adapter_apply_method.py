from th2_data_services.interfaces import IAdapter
from tests.tests_unit.tests_diff_version.conftest import http, START_TIME, END_TIME


class TestAdapterForEvents(IAdapter):
    def handle(self, record: dict) -> dict:
        if record.get("eventId"):
            return record


class TestAdapterForMessages(IAdapter):
    def handle(self, record: dict) -> dict:
        if record.get("messageId"):
            return record


def test_apply_for_GetEvents(data_source):
    ds = data_source
    ev_adapter = TestAdapterForEvents()
    events = ds.command(
        http.GetEvents(start_timestamp=START_TIME, end_timestamp=END_TIME, attached_messages=True).apply_adapter(
            ev_adapter.handle
        )
    )
    for event in events:
        assert isinstance(event, dict)


def test_apply_for_GetMessages(data_source):
    ds = data_source
    msg_adapter = TestAdapterForMessages()

    messages = ds.command(
        http.GetMessages(start_timestamp=START_TIME, end_timestamp=END_TIME, stream=["demo-conn2"]).apply_adapter(
            msg_adapter.handle
        )
    )
    for message in messages:
        assert isinstance(message, dict)
