from sseclient import Event
import pytest

from th2_data_services import Data, DataSource
from tests.conftest import START_TIME, END_TIME


def get_data_obj(rtype, ds, params_dict):
    if rtype == "events":
        return ds.get_events_from_data_provider(**params_dict)
    elif rtype == "messages":
        return ds.get_messages_from_data_provider(**params_dict)
    else:
        raise Exception("Not events or messages")


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
    def test_x_flag_true_or_default(self, demo_data_source: DataSource, params):
        ds = demo_data_source
        data: Data = get_data_obj(
            params[0],
            ds,
            dict(startTimestamp=START_TIME, endTimestamp=END_TIME, **params[1]),
        )

        for e in data:
            assert isinstance(e, dict)


class TestSSEFlagFalse:
    # @pytest.mark.parametrize("rtype", ['events', 'messages'])
    def test_events(self, demo_data_source: DataSource):
        ds = demo_data_source
        data: Data = ds.get_events_from_data_provider(
            startTimestamp=START_TIME,
            endTimestamp=END_TIME,
            sse_adapter=False,
        )

        for e in data:
            assert isinstance(e, Event)

    def test_messages_provider_not_none(self, demo_data_source: DataSource):
        ds = demo_data_source
        with pytest.raises(Exception) as exc_info:
            ds.get_messages_from_data_provider(
                startTimestamp=START_TIME,
                endTimestamp=END_TIME,
                stream=["demo-conn2"],
                sse_adapter=False,
            )

        assert "Provider adapter expected to get dict but SSE adapter is turned off" in str(exc_info)

    def test_messages_provider_none(self, demo_data_source: DataSource):
        ds = demo_data_source
        data: Data = ds.get_messages_from_data_provider(
            startTimestamp=START_TIME,
            endTimestamp=END_TIME,
            sse_adapter=False,
            stream=["demo-conn2"],
            provider_adapter=None,
        )

        for e in data:
            assert isinstance(e, Event)
