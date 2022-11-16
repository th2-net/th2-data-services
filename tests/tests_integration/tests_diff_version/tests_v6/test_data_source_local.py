import pytest

from ..conftest import HTTPProviderDataSource, http, Data
from th2_data_services.provider.exceptions import CommandError

from .. import EVENT_ID_TEST_DATA_ROOT, EVENT_ID_PLAIN_EVENT_1, MESSAGE_ID_1, MESSAGE_ID_2
from ..test_bodies.v6.test_event_bodies import root_event_body, plain_event_1_body, filter_event_3_body
from ..test_bodies.v6.test_message_bodies import message_1_body, message_2_body

<<<<<<< HEAD

def test_find_events_by_id_from_data_provider(data_source: HTTPProviderDataSource):
    data_source = data_source

=======
def test_find_events_by_id_from_data_provider(http_data_source: HTTPProviderDataSource):
>>>>>>> 382d800 (Updated v6 tests)
    expected_event = root_event_body

    expected_events = [expected_event, plain_event_1_body]

    event = http_data_source.command(http.GetEventById(EVENT_ID_TEST_DATA_ROOT))
    events = http_data_source.command(
        http.GetEventsById(
            [
                EVENT_ID_TEST_DATA_ROOT,
                EVENT_ID_PLAIN_EVENT_1,
            ]
        )
    )
    events_with_one_element = http_data_source.command(
        http.GetEventsById(
            [
                EVENT_ID_TEST_DATA_ROOT,
            ]
        )
    )
    for event_ in events:
        event_["attachedMessageIds"].sort()

    broken_event: dict = http_data_source.command(http.GetEventById("id", use_stub=True))
    broken_events: list = http_data_source.command(http.GetEventsById(["id", "ids"], use_stub=True))

    plug_for_broken_event: dict = {
        "attachedMessageIds": [],
        "batchId": "Broken_Event",
        "endTimestamp": {"nano": 0, "epochSecond": 0},
        "startTimestamp": {"nano": 0, "epochSecond": 0},
        "type": "event",
        "eventId": "id",
        "eventName": "Broken_Event",
        "eventType": "Broken_Event",
        "parentEventId": "Broken_Event",
        "successful": None,
        "isBatched": None,
    }

    plug_for_broken_events: list = [
        plug_for_broken_event.copy(),
        plug_for_broken_event.copy(),
    ]
    plug_for_broken_events[1]["eventId"] = "ids"

    # Check types
    assert isinstance(event, dict)
    assert isinstance(events, list)
    assert isinstance(events_with_one_element, list)
    assert isinstance(broken_event, dict)
    assert isinstance(broken_events, list)
    # Check content.
    assert event == expected_event
    assert events == expected_events
    assert len(events) == 2
    assert len(events_with_one_element) == 1
    # Check Broken_Events
    assert broken_event == plug_for_broken_event
    assert broken_events == plug_for_broken_events
    assert [event, broken_event] == http_data_source.command(
        http.GetEventsById([EVENT_ID_TEST_DATA_ROOT, "id"], use_stub=True)
    )
    with pytest.raises(CommandError):
        http_data_source.command(http.GetEventsById([EVENT_ID_TEST_DATA_ROOT, "id"]))
    with pytest.raises(CommandError):
        http_data_source.command(http.GetEventById("id"))


def test_find_messages_by_id_from_data_provider(http_data_source: HTTPProviderDataSource):
    expected_message = message_1_body

    expected_messages = [expected_message, message_2_body]

<<<<<<< HEAD
    message = data_source.command(http.GetMessageById(MESSAGE_ID_1))
    messages = data_source.command(http.GetMessagesById([MESSAGE_ID_1, MESSAGE_ID_2]))
    messages_with_one_element = data_source.command(http.GetMessagesById([MESSAGE_ID_1]))
=======
    message = http_data_source.command(http.GetMessageById(MESSAGE_ID_1))
    messages = http_data_source.command(
        http.GetMessagesById([MESSAGE_ID_1, MESSAGE_ID_2])
    )
    messages_with_one_element = http_data_source.command(http.GetMessagesById([MESSAGE_ID_1]))
>>>>>>> 382d800 (Updated v6 tests)
    # Check types
    assert isinstance(message, dict)
    assert isinstance(messages, list)
    assert isinstance(messages_with_one_element, list)
    # Check content.
    assert message == expected_message
    assert messages == expected_messages
    assert len(messages) == 2
    assert len(messages_with_one_element) == 1


def test_get_x_with_filters(
    get_events_with_one_filter: Data,
    get_messages_with_one_filter: Data,
    get_events_with_filters: Data,
    get_messages_with_filters: Data,
):
    event_case = [filter_event_3_body]
    message_case = [message_1_body]
    assert list(get_messages_with_one_filter) == message_case
    assert list(get_messages_with_filters) == message_case
    assert list(get_events_with_one_filter) == event_case and len(event_case) is 1
    assert list(get_events_with_filters) == event_case
