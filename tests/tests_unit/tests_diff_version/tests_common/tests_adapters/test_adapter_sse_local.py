from sseclient import Event as SSEEvent

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
