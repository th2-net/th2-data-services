from sseclient import Event
import pytest

from th2_data_services import Data, DataSource
from tests.conftest import START_TIME, END_TIME


class TestSSEFlagFalse:
    def test_events_provider_not_none(self, demo_data_source: DataSource):
        ds = demo_data_source
        with pytest.raises(Exception) as exc_info:
            ds.get_events_from_data_provider(
                startTimestamp=START_TIME,
                endTimestamp=END_TIME,
                sse_adapter=False,
            )

        assert "Provider adapter expected to get dict but SSE adapter is turned off" in str(exc_info)

    def test_events_provider_none(self, demo_data_source: DataSource):
        ds = demo_data_source
        data: Data = ds.get_events_from_data_provider(
            startTimestamp=START_TIME,
            endTimestamp=END_TIME,
            sse_adapter=False,
            provider_adapter=None,
        )

        for e in data:
            assert isinstance(e, Event)
