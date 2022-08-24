from datetime import datetime

import pytest
import requests

from th2_data_services.data import Data
from th2_data_services.provider.exceptions import CommandError
from tests.tests_unit.tests_diff_version.conftest import http, HTTPProviderDataSource


# TODO: Change on mock


def test_find_message_by_id_from_data_provider_with_error(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source

    with pytest.raises(CommandError) as exc_info:
        data_source.command(http.GetMessageById("demo-conn_not_exist:first:1624005448022245399"))


def test_get_events_from_data_provider_with_error(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source

    events = data_source.command(http.GetEvents(start_timestamp="test", end_timestamp="test"))
    with pytest.raises(TypeError) as exc_info:
        list(events)
    assert "replace() takes no keyword arguments" in str(exc_info)


def test_get_messages_from_data_provider_with_error(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source

    events = data_source.command(http.GetMessages(start_timestamp="test", end_timestamp="test", stream="test"))
    with pytest.raises(TypeError) as exc_info:
        list(events)
    assert "replace() takes no keyword arguments" in str(exc_info)


def test_check_url_for_data_source():
    with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
        data_source = HTTPProviderDataSource("http://test_test:8080/")
    assert "Max retries exceeded with url" in str(exc_info)


def test_messageIds_not_in_last_msg(demo_messages_from_data_source: Data):
    data = demo_messages_from_data_source
    data_lst = list(data)
    last_msg = data_lst[-1]
    assert "messageIds" not in last_msg


def test_get_messages_with_multiple_url(
    demo_messages_from_data_source_with_test_streams: Data,
    demo_messages_from_data_source: Data,
):
    messages = demo_messages_from_data_source_with_test_streams.use_cache(True)

    messages_hand_demo_expected = demo_messages_from_data_source
    messages_hand_demo_actual = messages.filter(lambda record: record.get("sessionId") == "arfq01fix07")

    assert (
        len(list(messages)) == 272
        and len(list(messages_hand_demo_actual)) == len(list(messages_hand_demo_expected)) == 239
    )


# def test_unprintable_character(demo_data_source: HTTPProviderDataSource):
#     event = demo_data_source.command(http.GetEventById(("b85d9dca-6236-11ec-bc58-1b1c943c5c0d")))
#
#     assert "\x80" in event["body"][0]["value"] and event["body"][0]["value"] == "nobJjpBJkTuQMmscc4R\x80"


def test_attached_messages(demo_data_source: HTTPProviderDataSource):
    events = demo_data_source.command(
        http.GetEvents(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=0, second=0, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=15, minute=0, second=0, microsecond=0),
            attached_messages=True,
        )
    )

    assert events.filter(lambda event: event.get("attachedMessageIds")).len
