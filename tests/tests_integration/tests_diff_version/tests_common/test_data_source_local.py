import pytest
import requests

from th2_data_services.data import Data
from th2_data_services.provider.exceptions import CommandError
from tests.tests_unit.tests_diff_version.conftest import http, HTTPProviderDataSource
from ..conftest import STREAM_1, STREAM_2


def test_issue_events(all_events):
    assert list(all_events.data) == all_events.expected_data_values


def test_issue_messages(all_messages):
    assert list(all_messages.data) == all_messages.expected_data_values


def test_find_message_by_id_from_data_provider_with_error(http_data_source: HTTPProviderDataSource):
    with pytest.raises(CommandError) as exc_info:
        http_data_source.command(http.GetMessageById("demo-conn_not_exist:first:1624005448022245399"))


def test_get_events_from_data_provider_with_error(http_data_source: HTTPProviderDataSource):
    events = http_data_source.command(http.GetEvents(start_timestamp="test", end_timestamp="test"))
    with pytest.raises(TypeError) as exc_info:
        list(events)
    assert "replace() takes no keyword arguments" in str(exc_info)


def test_get_messages_from_data_provider_with_error(http_data_source: HTTPProviderDataSource):
    events = http_data_source.command(http.GetMessages(start_timestamp="test", end_timestamp="test", stream="test"))
    with pytest.raises(TypeError) as exc_info:
        list(events)
    assert "replace() takes no keyword arguments" in str(exc_info)


def test_check_url_for_http_data_source():
    with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
        http_data_source = HTTPProviderDataSource("http://test_test:8080/")
    assert "Max retries exceeded with url" in str(exc_info)


def test_messageIds_not_in_last_msg(messages_from_data_source: Data):
    data = messages_from_data_source
    data_lst = list(data)
    last_msg = data_lst[-1]
    assert "messageIds" not in last_msg


def test_get_messages_with_multiple_url(
    messages_from_data_source_with_streams: Data,
    messages_from_data_source: Data,
):
    messages = messages_from_data_source_with_streams.use_cache(True)

    messages_hand_expected = messages_from_data_source
    messages_hand_actual = messages.filter(
        lambda record: record.get("sessionId") == STREAM_1 or record.get("sessionId") == STREAM_2
    )

    assert len(list(messages)) == 6 and len(list(messages_hand_actual)) == len(list(messages_hand_expected)) == 6


# def test_unprintable_character(http_data_source: HTTPProviderDataSource):
#     event = http_data_source.command(http.GetEventById(("b85d9dca-6236-11ec-bc58-1b1c943c5c0d")))
#
#     assert "\x80" in event["body"][0]["value"] and event["body"][0]["value"] == "nobJjpBJkTuQMmscc4R\x80"

"""NO ATTACHED MESSAGES ON EVENTS YET
def test_attached_messages(http_data_source: HTTPProviderDataSource):
    events = http_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            attached_messages=True,
        )
    )

    assert events.filter(lambda event: event.get("attachedMessageIds")).len
"""


def test_events_for_data_loss(all_events):
    """Check that Data object won't loss its stream.

    It might happen if source inside of Data is object of generator instead of
    generator function.
    """
    events = all_events.data
    for _ in range(3):
        for _ in events:
            pass

    assert list(events) == all_events.expected_data_values


def test_messages_for_data_loss(all_messages):
    """Check that Data object won't loss its stream.

    It might happen if source inside of Data is object of generator instead of
    generator function.
    """
    messages = all_messages.data
    for _ in range(3):
        for _ in messages:
            pass

    assert list(messages) == all_messages.expected_data_values
