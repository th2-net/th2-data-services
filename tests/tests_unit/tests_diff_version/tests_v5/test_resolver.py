from th2_data_services.provider.v5.resolver import Provider5EventFieldsResolver, Provider5MessageFieldsResolver
import inspect

def test_resolver_event():
    event = {
        "type": "event",
        "eventId": "9daac0e5-65ad-11ed-a742-b48c9dc9ebfb",
        "batchId": None,
        "isBatched": False,
        "eventName": "Set of auto-generated events for ds lib testing",
        "eventType": "ds-lib-test-event",
        "endTimestamp": {"nano": 307080000, "epochSecond": 1668603187},
        "startTimestamp": {"nano": 307080000, "epochSecond": 1668603187},
        "parentEventId": None,
        "successful": True,
        "attachedMessageIds": [],
        "body": {},
    }

    expected_values = {
        'get_attached_messages_ids': [],
        'get_batch_id': None,
        'get_body': {},
        'get_end_timestamp': {
            'nano': 307080000,
            'epochSecond': 1668603187
        },
        'get_id': '9daac0e5-65ad-11ed-a742-b48c9dc9ebfb',
        'get_is_batched': False,
        'get_name': 'Set of auto-generated events for ds lib testing',
        'get_parent_id': None,
        'get_start_timestamp': {
            'nano': 307080000,
            'epochSecond': 1668603187
        },
        'get_status': True,
        'get_type': 'ds-lib-test-event'
    }

    for function_name,function in inspect.getmembers(Provider5EventFieldsResolver, predicate=inspect.isfunction):
        assert function(event) == expected_values[function_name]

def test_resolver_message():
    message = {
        "type": "message",
        "timestamp": {"nano": 307080000, "epochSecond": 1668603187},
        "messageType": "Incoming",
        "direction": "IN",
        "sessionId": "ds-lib-session1",
        "attachedEventIds": [],
        "messageId": "ds-lib-session1:first:1668603186732416805",
        "body": {
            "metadata": {
                "id": {"connectionId": {"sessionAlias": "ds-lib-session1"}, "sequence": "1668603186732416805"},
                "messageType": "Incoming",
                "protocol": "json",
            },
            "fields": {"msg_for_get_by_id_num": {"simpleValue": "1"}},
        },
        "bodyBase64": "eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMSJ9",
    }
    
    expected_values = {
        'get_attached_event_ids': [],
        'get_body': {
            'metadata': {
                'id': {
                    'connectionId': {
                        'sessionAlias': 'ds-lib-session1'
                    },
                    'sequence': '1668603186732416805'
                },
                'messageType': 'Incoming',
                'protocol': 'json'
            },
            'fields': {
                'msg_for_get_by_id_num': {
                    'simpleValue': '1'
                }
            }
        },
        'get_body_base64': 'eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMSJ9',
        'get_connection_id': {
            'sessionAlias': 'ds-lib-session1'
        },
        'get_direction': 'IN',
        'get_fields': {
            'msg_for_get_by_id_num': {
                'simpleValue': '1'
            }
        },
        'get_id': 'ds-lib-session1:first:1668603186732416805',
        'get_sequence': '1668603186732416805',
        'get_session_alias': 'ds-lib-session1',
        'get_session_id': 'ds-lib-session1',
        'get_subsequence': None,
        'get_timestamp': {
            'nano': 307080000,
            'epochSecond': 1668603187
        },
        'get_type': 'Incoming'
    }

    for function_name,function in inspect.getmembers(Provider5MessageFieldsResolver, predicate=inspect.isfunction):
        assert function(message) == expected_values[function_name]