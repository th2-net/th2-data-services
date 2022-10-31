from sseclient import Event as SSEEvent

from th2_data_services.interfaces import IAdapter

import pytest

from th2_data_services import Data
from tests.tests_unit.tests_diff_version.conftest import HTTPProviderDataSource, http, START_TIME, END_TIME


@pytest.mark.skip
def get_data_obj(rtype, ds, params_dict):
    if rtype == "events":
        return ds.command(
            http.GetEvents(start_timestamp=params_dict["startTimestamp"], end_timestamp=params_dict["endTimestamp"])
        )
    elif rtype == "messages":
        return ds.command(
            http.GetMessages(
                start_timestamp=params_dict["startTimestamp"],
                end_timestamp=params_dict["endTimestamp"],
                stream=params_dict["stream"],
            )
        )
    else:
        raise Exception("Not events or messages")


@pytest.mark.skip
class TestSSEFlagTrue:
    @pytest.mark.parametrize(
        "params",
        [
            ("events", dict(sse_adapter=True)),
            ("events", dict()),
            (
                "messages",
                dict(
                    sse_adapter=True,
                    stream=["demo-conn2"],
                    provider_adapter=None,
                ),
            ),
            (
                "messages",
                dict(
                    stream=["demo-conn2"],
                    provider_adapter=None,
                ),
            ),
        ],
    )
    def test_x_flag_true_or_default(self, demo_data_source: HTTPProviderDataSource, params):
        ds = demo_data_source
        data: Data = get_data_obj(params[0], ds, dict(startTimestamp=START_TIME, endTimestamp=END_TIME, **params[1]))

        for e in data:
            assert isinstance(e, dict)


@pytest.mark.skip
class TestSSEFlagFalse:
    # @pytest.mark.parametrize("rtype", ['events', 'messages'])
    def test_events(self, demo_data_source: HTTPProviderDataSource):
        ds = demo_data_source
        data: Data = ds.command(
            http.GetEventsSSEEvents(
                start_timestamp=START_TIME,
                end_timestamp=END_TIME,
            )
        )

        for e in data:
            assert isinstance(e, SSEEvent)

    def test_messages_provider_none(self, demo_data_source: HTTPProviderDataSource):
        ds = demo_data_source
        data: Data = ds.command(
            http.GetMessages(
                start_timestamp=START_TIME,
                end_timestamp=END_TIME,
                stream=["demo-conn2"],
            )
        )

        for e in data:
            assert isinstance(e, SSEEvent)


class TestAdapterForEvents(IAdapter):
    def handle(self, record: SSEEvent) -> SSEEvent:
        if record.event == "event":
            return record
        else:
            return SSEEvent(event="close")


class TestAdapterForMessages(IAdapter):
    def handle(self, record: SSEEvent) -> SSEEvent:
        print(record.event)
        if record.event == "message":
            return record
        else:
            return SSEEvent(event="close")


def test_adapter(demo_data_source):
    ds = demo_data_source
    ev_adapter = TestAdapterForEvents()
    msg_adapter = TestAdapterForMessages()

    events = ds.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
        ).apply_adapter(ev_adapter.handle)
    )
    messages = ds.command(
        http.GetMessages(start_timestamp=START_TIME, end_timestamp=END_TIME, stream=["demo-conn2"]).apply_adapter(
            msg_adapter.handle
        )
    )
    for event in events:
        assert isinstance(event, dict)
    for message in messages:
        assert isinstance(message, dict)
