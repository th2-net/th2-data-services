from th2_data_services.provider.v6.resolver import Provider6EventFieldsResolver, Provider6MessageFieldsResolver
import inspect

def test_resolver_event():
    event = {
        "type": "event",
        "eventId": "a26078a4-6419-11ed-bfec-b48c9dc9ebfb",
        "batchId": None,
        "isBatched": False,
        "eventName": "Set of auto-generated events for ds lib testing",
        "eventType": "ds-lib-test-event",
        "endTimestamp": "2022-11-14T12:41:18.095247000Z",
        "startTimestamp": "2022-11-14T12:41:18.095247000Z",
        "parentEventId": None,
        "successful": True,
        "attachedMessageIds": [],
        "body": {},
    }

    expected_values = {
        'get_attached_messages_ids': [],
        'get_batch_id': None,
        'get_body': {},
        'get_end_timestamp': '2022-11-14T12:41:18.095247000Z',
        'get_id': 'a26078a4-6419-11ed-bfec-b48c9dc9ebfb',
        'get_is_batched': False,
        'get_name': 'Set of auto-generated events for ds lib testing',
        'get_parent_id': None,
        'get_start_timestamp': '2022-11-14T12:41:18.095247000Z',
        'get_status': True,
        'get_type': 'ds-lib-test-event'
    }

    for function_name,function in inspect.getmembers(Provider6EventFieldsResolver, predicate=inspect.isfunction):
        assert function(event) == expected_values[function_name]

def test_resolver_message():
    message = {
        "type": "message",
        "id": "ds-lib-session1:first:1668429677955474105",
        "timestamp": "2022-11-14T12:41:18.094248000Z",
        "sessionId": "ds-lib-session1",
        "direction": "FIRST",
        "sequence": "1668429677955474105",
        "attachedEventIds": [],
        "rawMessageBase64": "eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMSJ9",
        "parsedMessages": [
            {
                "match": True,
                "id": "ds-lib-session1:first:1668429677955474105.",
                "message": {
                    "metadata": {
                        "id": {"connectionId": {"sessionAlias": "ds-lib-session1"}, "sequence": "1668429677955474105"},
                        "messageType": "Incoming",
                        "properties": {"com.exactpro.th2.cradle.grpc.protocol": "json"},
                        "protocol": "json",
                    },
                    "fields": {"msg_for_get_by_id_num": {"simpleValue": "1"}},
                },
            }
        ],
    }
    
    expected_values = {
        'get_attached_event_ids': [],
        'get_body': [{
            'match': True,
            'id': 'ds-lib-session1:first:1668429677955474105.',
            'message': {
                'metadata': {
                    'id': {
                        'connectionId': {
                            'sessionAlias': 'ds-lib-session1'
                        },
                        'sequence': '1668429677955474105'
                    },
                    'messageType': 'Incoming',
                    'properties': {
                        'com.exactpro.th2.cradle.grpc.protocol': 'json'
                    },
                    'protocol': 'json'
                },
                'fields': {
                    'msg_for_get_by_id_num': {
                        'simpleValue': '1'
                    }
                }
            }
        }],
        'get_body_base64': 'eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMSJ9',
        'get_connection_id': {
            'sessionAlias': 'ds-lib-session1'
        },
        'get_direction': 'FIRST',
        'get_fields': {
            'msg_for_get_by_id_num': {
                'simpleValue': '1'
            }
        },
        'get_id': 'ds-lib-session1:first:1668429677955474105',
        'get_sequence': '1668429677955474105',
        'get_session_alias': 'ds-lib-session1',
        'get_session_id': 'ds-lib-session1',
        'get_subsequence': None,
        'get_timestamp': '2022-11-14T12:41:18.094248000Z',
        'get_type': 'Incoming'
    }

    for function_name,function in inspect.getmembers(Provider6MessageFieldsResolver, predicate=inspect.isfunction):
        assert function(message) == expected_values[function_name]