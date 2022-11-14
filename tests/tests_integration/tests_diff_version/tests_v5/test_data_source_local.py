import pytest

from ..conftest import HTTPProviderDataSource, http, Data
from th2_data_services.provider.exceptions import CommandError

EVENT_ID_1 = '2479e531-6017-11ed-9d54-b48c9dc9ebfa'
EVENT_ID_2 = '24aae778-6017-11ed-b87c-b48c9dc9ebfa'
MESSAGE_ID_1 = 'ds-lib-session1:first:1668068118435545201'
MESSAGE_ID_2 = 'ds-lib-session1:first:1668068118435545202'

def test_find_events_by_id_from_data_provider(data_source: HTTPProviderDataSource):
    data_source = data_source

    expected_event = {
        'attachedMessageIds': [],
        'batchId': None,
        'body': {},
        'endTimestamp': {'epochSecond': 1667988803, 'nano': 83601000},
        'eventId': '2479e531-6017-11ed-9d54-b48c9dc9ebfa',
        'eventName': 'Set of auto-generated events for ds lib testing',
        'eventType': 'ds-lib-test-event',
        'isBatched': False,
        'parentEventId': None,
        'startTimestamp': {'epochSecond': 1667988803, 'nano': 83601000},
        'successful': True,
        'type': 'event'
    }

    expected_events = []
    expected_events.append(expected_event)
    expected_events.append(
        {
            'attachedMessageIds': [],
            'batchId': None,
            'body': 'ds-lib test body',
            'endTimestamp': {'epochSecond': 1667988803, 'nano': 404786000},
            'eventId': '24aae778-6017-11ed-b87c-b48c9dc9ebfa',
            'eventName': 'Plain event 1',
            'eventType': 'ds-lib-test-event',
            'isBatched': False,
            'parentEventId': '2479e531-6017-11ed-9d54-b48c9dc9ebfa',
            'startTimestamp': {'epochSecond': 1667988803, 'nano': 404786000},
            'successful': True,
            'type': 'event'
        }
    )

    event = data_source.command(http.GetEventById(EVENT_ID_1))
    events = data_source.command(
        http.GetEventsById(
            [
                EVENT_ID_1,
                EVENT_ID_2,
            ]
        )
    )
    events_with_one_element = data_source.command(
        http.GetEventsById(
            [
                EVENT_ID_1,
            ]
        )
    )
    for event_ in events:
        event_["attachedMessageIds"].sort()

    broken_event: dict = data_source.command(http.GetEventById("id", use_stub=True))
    broken_events: list = data_source.command(http.GetEventsById(["id", "ids"], use_stub=True))

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
    assert [event, broken_event] == data_source.command(
        http.GetEventsById([EVENT_ID_1, "id"], use_stub=True)
    )
    with pytest.raises(CommandError):
        data_source.command(http.GetEventsById([EVENT_ID_1, "id"]))
    with pytest.raises(CommandError):
        data_source.command(http.GetEventById("id"))


def test_find_messages_by_id_from_data_provider(data_source: HTTPProviderDataSource):
    data_source = data_source

    expected_message = {
        'type': 'message',
        'timestamp': {
            'nano': 435545000,
            'epochSecond': 1668068118
        },
        'messageType': 'Incoming',
        'direction': 'IN',
        'sessionId': 'ds-lib-session1',
        'attachedEventIds': [],
        'messageId': 'ds-lib-session1:first:1668068118435545201',
        'body': {
            'metadata': {
                'id': {
                    'connectionId': {
                        'sessionAlias': 'ds-lib-session1'
                    },
                    'sequence': '1668068118435545201'
                },
                'messageType': 'Incoming',
                'protocol': 'json'
            },
            'fields': {
                'a': {
                    'simpleValue': '123'
                }
            }
        },
        'bodyBase64': 'eyJhIjogIjEyMyJ9'
    }

    expected_messages = []
    expected_messages.append(expected_message)
    expected_messages.append(
        {
            'type': 'message',
            'timestamp': {
                'nano': 802350000,
                'epochSecond': 1668068118
            },
            'messageType': 'Incoming',
            'direction': 'IN',
            'sessionId': 'ds-lib-session2',
            'attachedEventIds': [],
            'messageId': 'ds-lib-session2:first:1668068118435545202',
            'body': {
                'metadata': {
                    'id': {
                        'connectionId': {
                            'sessionAlias': 'ds-lib-session2'
                        },
                        'sequence': '1668068118435545202'
                    },
                    'messageType': 'Incoming',
                    'protocol': 'json'
                },
                'fields': {
                    'a': {
                        'simpleValue': '123'
                    }
                }
            },
            'bodyBase64': 'eyJhIjogIjEyMyJ9'
        }
    )

    message = data_source.command(http.GetMessageById(MESSAGE_ID_1))
    messages = data_source.command(
        http.GetMessagesById([MESSAGE_ID_1, MESSAGE_ID_2])
    )
    messages_with_one_element = data_source.command(http.GetMessagesById([MESSAGE_ID_1]))
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
    case = [
        {
            "type": "event",
            "eventId": "24ab19ed-6017-11ed-98bf-b48c9dc9ebfa",
            "batchId": "None",
            "isBatched": False,
            "eventName": "Event for Filter test. FilterString-3",
            "eventType": "ds-lib-test-event",
            "endTimestamp": {
                "nano": 406077000,
                "epochSecond": 1667988803
            },
            "startTimestamp": {
                "nano": 406077000,
                "epochSecond": 1667988803
            },
            "parentEventId": "2479e531-6017-11ed-9d54-b48c9dc9ebfa",
            "successful": True,
            "attachedMessageIds": [],
            "body": "ds-lib test body. FilterString-3"                                                          
        }
    ]
    case1 = [
        {
            'type': 'message',
            'timestamp': {
                'nano': 435545000,
                'epochSecond': 1668068118
            },
            'messageType': 'Incoming',
            'direction': 'IN',
            'sessionId': 'ds-lib-session1',
            'attachedEventIds': [],
            'messageId': 'ds-lib-session1:first:1668068118435545201',
            'body': {
                'metadata': {
                    'id': {
                        'connectionId': {
                            'sessionAlias': 'ds-lib-session1'
                        },
                        'sequence': '1668068118435545201'
                    },
                    'messageType': 'Incoming',
                    'protocol': 'json'
                },
                'fields': {
                    'a': {
                        'simpleValue': '123'
                    }
                }
            },
            'bodyBase64': 'eyJhIjogIjEyMyJ9'
        }
    ]
    assert list(get_messages_with_one_filter) == case1
    assert list(get_messages_with_filters) == case1
    assert list(get_events_with_one_filter) == case and len(case) is 1
    assert list(get_events_with_filters) == case
