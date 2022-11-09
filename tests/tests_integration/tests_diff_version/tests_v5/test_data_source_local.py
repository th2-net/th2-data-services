import pytest

from ..conftest import HTTPProviderDataSource, http, Data
from th2_data_services.provider.exceptions import CommandError


def test_find_events_by_id_from_data_provider(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source

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

    event = data_source.command(http.GetEventById("2479e531-6017-11ed-9d54-b48c9dc9ebfa"))
    events = data_source.command(
        http.GetEventsById(
            [
                "2479e531-6017-11ed-9d54-b48c9dc9ebfa",
                "24aae778-6017-11ed-b87c-b48c9dc9ebfa",
            ]
        )
    )
    events_with_one_element = data_source.command(
        http.GetEventsById(
            [
                "2479e531-6017-11ed-9d54-b48c9dc9ebfa",
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
        http.GetEventsById(["2479e531-6017-11ed-9d54-b48c9dc9ebfa", "id"], use_stub=True)
    )
    with pytest.raises(CommandError):
        data_source.command(http.GetEventsById(["2479e531-6017-11ed-9d54-b48c9dc9ebfa", "id"]))
    with pytest.raises(CommandError):
        data_source.command(http.GetEventById("id"))


def test_find_messages_by_id_from_data_provider(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source

    expected_message = {
        "attachedEventIds": [],
        "body": {
            "fields": {
                "header": {
                    "messageValue": {
                        "fields": {
                            "BeginString": {"simpleValue": "FIXT.1.1"},
                            "BodyLength": {"simpleValue": "61"},
                            "MsgSeqNum": {"simpleValue": "33"},
                            "MsgType": {"simpleValue": "0"},
                            "SenderCompID": {"simpleValue": "ARFQ01FIX08"},
                            "SendingTime": {"simpleValue": "2022-06-30T14:39:27.111"},
                            "TargetCompID": {"simpleValue": "FGW"},
                        }
                    }
                },
                "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "160"}}}},
            },
            "metadata": {
                "id": {
                    "connectionId": {"sessionAlias": "arfq01fix08"},
                    "direction": "SECOND",
                    "sequence": "1656599887515499033",
                    "subsequence": [1],
                },
                "messageType": "Heartbeat",
                "protocol": "FIX",
                "timestamp": "2022-06-30T14:39:27.112Z",
            },
        },
        "bodyBase64": "OD1GSVhULjEuMQE5PTYxATM1PTABMzQ9MzMBNDk9QVJGUTAxRklYMDgBNTI9MjAyMjA2MzAtMTQ6Mzk6MjcuMTExMDAwATU2PUZHVwExMD0xNjAB",
        "direction": "OUT",
        "messageId": "arfq01fix08:second:1656599887515499033",
        "messageType": "Heartbeat",
        "sessionId": "arfq01fix08",
        "timestamp": {"epochSecond": 1656599967, "nano": 112000000},
        "type": "message",
    }

    expected_messages = []
    expected_messages.append(expected_message)
    expected_messages.append(
        {
            "attachedEventIds": [],
            "body": {
                "fields": {
                    "DefaultApplVerID": {"simpleValue": "9"},
                    "EncryptMethod": {"simpleValue": "0"},
                    "HeartBtInt": {"simpleValue": "5"},
                    "Password": {"simpleValue": "mit123"},
                    "ResetSeqNumFlag": {"simpleValue": "true"},
                    "header": {
                        "messageValue": {
                            "fields": {
                                "BeginString": {"simpleValue": "FIXT.1.1"},
                                "BodyLength": {"simpleValue": "91"},
                                "MsgSeqNum": {"simpleValue": "1"},
                                "MsgType": {"simpleValue": "A"},
                                "SenderCompID": {"simpleValue": "ARFQ01DC03"},
                                "SendingTime": {"simpleValue": "2022-06-30T14:46:03.911"},
                                "TargetCompID": {"simpleValue": "FGW"},
                            }
                        }
                    },
                    "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "161"}}}},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "arfq01dc03"},
                        "direction": "SECOND",
                        "sequence": "1656599850628059096",
                        "subsequence": [1],
                    },
                    "messageType": "Logon",
                    "protocol": "FIX",
                    "timestamp": "2022-06-30T14:46:03.915Z",
                },
            },
            "bodyBase64": "OD1GSVhULjEuMQE5PTkxATM1PUEBMzQ9MQE0OT1BUkZRMDFEQzAzATUyPTIwMjIwNjMwLTE0OjQ2OjAzLjkxMQE1Nj1GR1cBOTg9MAExMDg9NQExNDE9WQE1NTQ9bWl0MTIzATExMzc9OQExMD0xNjEB",
            "direction": "OUT",
            "messageId": "arfq01dc03:second:1656599850628059096",
            "messageType": "Logon",
            "sessionId": "arfq01dc03",
            "timestamp": {"epochSecond": 1656600363, "nano": 915000000},
            "type": "message",
        }
    )

    message = data_source.command(http.GetMessageById("arfq01fix08:second:1656599887515499033"))
    messages = data_source.command(
        http.GetMessagesById(["arfq01fix08:second:1656599887515499033", "arfq01dc03:second:1656599850628059096"])
    )
    messages_with_one_element = data_source.command(http.GetMessagesById(["arfq01fix08:second:1656599887515499033"]))
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
    demo_get_events_with_one_filter: Data,
    demo_get_messages_with_one_filter: Data,
    demo_get_events_with_filters: Data,
    demo_get_messages_with_filters: Data,
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
            "type": "message",
            "timestamp": {"nano": 422000000, "epochSecond": 1656600504},
            "messageType": "NewOrderSingle",
            "direction": "OUT",
            "sessionId": "arfq01fix07",
            "attachedEventIds": [],
            "messageId": "arfq01fix07:second:1656599837520228626",
            "body": {
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "arfq01fix07"},
                        "direction": "SECOND",
                        "sequence": "1656599837520228626",
                        "subsequence": [1],
                    },
                    "timestamp": "2022-06-30T14:48:24.422Z",
                    "messageType": "NewOrderSingle",
                    "protocol": "FIX",
                },
                "fields": {
                    "OrderQty": {"simpleValue": "200"},
                    "OrdType": {"simpleValue": "2"},
                    "ClOrdID": {"simpleValue": "1830410"},
                    "SecurityIDSource": {"simpleValue": "8"},
                    "OrderCapacity": {"simpleValue": "A"},
                    "TransactTime": {"simpleValue": "2022-06-30T14:47:59.032276"},
                    "SecondaryClOrdID": {"simpleValue": "11111"},
                    "AccountType": {"simpleValue": "1"},
                    "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "152"}}}},
                    "Side": {"simpleValue": "1"},
                    "Price": {"simpleValue": "55"},
                    "TradingParty": {
                        "messageValue": {
                            "fields": {
                                "NoPartyIDs": {
                                    "listValue": {
                                        "values": [
                                            {
                                                "messageValue": {
                                                    "fields": {
                                                        "PartyRole": {"simpleValue": "76"},
                                                        "PartyID": {"simpleValue": "ARFQ01FIX07"},
                                                        "PartyIDSource": {"simpleValue": "D"},
                                                    }
                                                }
                                            },
                                            {
                                                "messageValue": {
                                                    "fields": {
                                                        "PartyRole": {"simpleValue": "3"},
                                                        "PartyID": {"simpleValue": "0"},
                                                        "PartyIDSource": {"simpleValue": "P"},
                                                    }
                                                }
                                            },
                                            {
                                                "messageValue": {
                                                    "fields": {
                                                        "PartyRole": {"simpleValue": "122"},
                                                        "PartyID": {"simpleValue": "0"},
                                                        "PartyIDSource": {"simpleValue": "P"},
                                                    }
                                                }
                                            },
                                            {
                                                "messageValue": {
                                                    "fields": {
                                                        "PartyRole": {"simpleValue": "12"},
                                                        "PartyID": {"simpleValue": "3"},
                                                        "PartyIDSource": {"simpleValue": "P"},
                                                    }
                                                }
                                            },
                                        ]
                                    }
                                }
                            }
                        }
                    },
                    "SecurityID": {"simpleValue": "5221001"},
                    "header": {
                        "messageValue": {
                            "fields": {
                                "BeginString": {"simpleValue": "FIXT.1.1"},
                                "SenderCompID": {"simpleValue": "ARFQ01FIX07"},
                                "SendingTime": {"simpleValue": "2022-06-30T14:48:24.330"},
                                "TargetCompID": {"simpleValue": "FGW"},
                                "MsgType": {"simpleValue": "D"},
                                "MsgSeqNum": {"simpleValue": "626"},
                                "BodyLength": {"simpleValue": "263"},
                            }
                        }
                    },
                    "DisplayQty": {"simpleValue": "200"},
                },
            },
            "bodyBase64": "OD1GSVhULjEuMQE5PTI2MwEzNT1EATM0PTYyNgE0OT1BUkZRMDFGSVgwNwE1Mj0yMDIyMDYzMC0xNDo0ODoyNC4zMzAwMDABNTY9RkdXATExPTE4MzA0MTABMjI9OAEzOD0yMDABNDA9MgE0ND01NQE0OD01MjIxMDAxATU0PTEBNjA9MjAyMjA2MzAtMTQ6NDc6NTkuMDMyMjc2ATUyNj0xMTExMQE1Mjg9QQE1ODE9MQExMTM4PTIwMAE0NTM9NAE0NDg9QVJGUTAxRklYMDcBNDQ3PUQBNDUyPTc2ATQ0OD0wATQ0Nz1QATQ1Mj0zATQ0OD0wATQ0Nz1QATQ1Mj0xMjIBNDQ4PTMBNDQ3PVABNDUyPTEyATEwPTE1MgE=",
        }
    ]
    assert list(demo_get_messages_with_one_filter) == case1
    assert list(demo_get_messages_with_filters) == case1
    assert list(demo_get_events_with_one_filter) == case and len(case) is 1
    assert list(demo_get_events_with_filters) == case
