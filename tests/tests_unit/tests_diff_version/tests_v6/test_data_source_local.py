import pytest

from ..conftest import HTTPProviderDataSource, http, Data
from th2_data_services.provider.exceptions import CommandError

"""
Slava Ermakov 2022.10.31

All tests below were skipped because there was a plan to change 
DataSource classes to mocks.

The same tests are placed in tests/tests_integration 
"""


@pytest.mark.skip(reason="data_source should be changed to mock")
def test_find_events_by_id_from_data_provider(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source  # TODO: Change on mock

    expected_event = {
        "attachedMessageIds": [],
        "batchId": None,
        "body": {},
        "endTimestamp": "2022-06-30T14:37:31.420806000Z",
        "eventId": "2c4b3a58-f882-11ec-b952-0a1e730db2c6",
        "eventName": "Recon: Test",
        "eventType": "",
        "isBatched": False,
        "parentEventId": None,
        "startTimestamp": "2022-06-30T14:37:31.420806000Z",
        "successful": False,
        "type": "event",
    }

    expected_events = []
    expected_events.append(expected_event)
    expected_events.append(
        {
            "type": "event",
            "eventId": "a5586d90-b83b-48a4-bd2b-b2059fb79374:b84cff2c-f883-11ec-b070-0a1e730db2c6",
            "batchId": "a5586d90-b83b-48a4-bd2b-b2059fb79374",
            "isBatched": True,
            "eventName": "Match by ClOrdID: '7706360'",
            "eventType": "",
            "endTimestamp": "2022-06-30T14:48:35.809998000Z",
            "startTimestamp": "2022-06-30T14:48:35.809998000Z",
            "parentEventId": "b21a03c0-f883-11ec-b070-0a1e730db2c6",
            "successful": True,
            "attachedMessageIds": ["arfq01fix08:first:1656599887515453583", "arfq01fix08:second:1656599887515499581"],
            "body": {
                "type": "table",
                "rows": [
                    {"Name": "ClOrdId", "Value": "7706360"},
                    {"Name": "Message Response", "Value": "ExecutionReport"},
                    {"Name": "Message Request", "Value": "NewOrderSingle"},
                    {"Name": "Latency type", "Value": "Trade"},
                    {"Name": "Latency", "Value": 29000.0},
                ],
                "_TableComponent__column_names": ["Name", "Value"],
            },
        }
    )

    event = data_source.command(http.GetEventById("2c4b3a58-f882-11ec-b952-0a1e730db2c6"))
    events = data_source.command(
        http.GetEventsById(
            [
                "2c4b3a58-f882-11ec-b952-0a1e730db2c6",
                "a5586d90-b83b-48a4-bd2b-b2059fb79374:b84cff2c-f883-11ec-b070-0a1e730db2c6",
            ]
        )
    )
    events_with_one_element = data_source.command(
        http.GetEventsById(
            [
                "2c4b3a58-f882-11ec-b952-0a1e730db2c6",
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
        http.GetEventsById(["2c4b3a58-f882-11ec-b952-0a1e730db2c6", "id"], use_stub=True)
    )
    with pytest.raises(CommandError):
        data_source.command(http.GetEventsById(["2c4b3a58-f882-11ec-b952-0a1e730db2c6", "id"]))
    with pytest.raises(CommandError):
        data_source.command(http.GetEventById("id"))


@pytest.mark.skip(reason="data_source should be changed to mock")
def test_find_messages_by_id_from_data_provider(demo_data_source: HTTPProviderDataSource):
    data_source = demo_data_source  # TODO: Change on mock

    expected_message = {
        "attachedEventIds": [],
        "direction": "SECOND",
        "id": "arfq01fix08:second:1656599887515499033",
        "parsedMessages": [
            {
                "id": "arfq01fix08:second:1656599887515499033.1",
                "match": True,
                "message": {
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
            }
        ],
        "rawMessageBase64": "OD1GSVhULjEuMQE5PTYxATM1PTABMzQ9MzMBNDk9QVJGUTAxRklYMDgBNTI9MjAyMjA2MzAtMTQ6Mzk6MjcuMTExMDAwATU2PUZHVwExMD0xNjAB",
        "sequence": "1656599887515499033",
        "sessionId": "arfq01fix08",
        "timestamp": "2022-06-30T14:39:27.112000000Z",
        "type": "message",
    }

    expected_messages = []
    expected_messages.append(expected_message)
    expected_messages.append(
        {
            "attachedEventIds": [],
            "direction": "SECOND",
            "id": "arfq01dc03:second:1656599850628059096",
            "parsedMessages": [
                {
                    "id": "arfq01dc03:second:1656599850628059096.1",
                    "match": True,
                    "message": {
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
                }
            ],
            "rawMessageBase64": "OD1GSVhULjEuMQE5PTkxATM1PUEBMzQ9MQE0OT1BUkZRMDFEQzAzATUyPTIwMjIwNjMwLTE0OjQ2OjAzLjkxMQE1Nj1GR1cBOTg9MAExMDg9NQExNDE9WQE1NTQ9bWl0MTIzATExMzc9OQExMD0xNjEB",
            "sequence": "1656599850628059096",
            "sessionId": "arfq01dc03",
            "timestamp": "2022-06-30T14:46:03.915000000Z",
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


@pytest.mark.skip(reason="data_source should be changed to mock")
def test_get_x_with_filters(
    demo_get_events_with_one_filter: Data,
    demo_get_messages_with_one_filter: Data,
    demo_get_events_with_filters: Data,
    demo_get_messages_with_filters: Data,
):
    # TODO: Change on mock
    case = [
        {
            "type": "event",
            "eventId": "a2321a5b-f883-11ec-8225-52540095fac0",
            "batchId": None,
            "isBatched": False,
            "eventName": "[TS_1]5 partfill trades and cancel.",
            "eventType": "",
            "endTimestamp": "2022-06-30T14:47:58.735114000Z",
            "startTimestamp": "2022-06-30T14:47:58.735039000Z",
            "parentEventId": None,
            "successful": False,
            "attachedMessageIds": [],
            "body": {},
        }
    ]
    case1 = [
        {
            "type": "event",
            "eventId": "bb0da3a9-f883-11ec-aeb3-adf8526f5eec",
            "batchId": None,
            "isBatched": False,
            "eventName": "Received 'ExecutionReport' response message",
            "eventType": "message",
            "endTimestamp": "2022-06-30T14:48:40.428471000Z",
            "startTimestamp": "2022-06-30T14:48:40.428350000Z",
            "parentEventId": "ba4e7257-f883-11ec-aeb3-adf8526f5eec",
            "successful": True,
            "attachedMessageIds": [],
            "body": [
                {
                    "type": "treeTable",
                    "rows": {
                        "ExecID": {"type": "row", "columns": {"fieldValue": "E0AmqxctTQGw"}},
                        "OrderQty": {"type": "row", "columns": {"fieldValue": "20"}},
                        "LastQty": {"type": "row", "columns": {"fieldValue": "20"}},
                        "OrderID": {"type": "row", "columns": {"fieldValue": "00Amr2Sw36j1"}},
                        "TransactTime": {"type": "row", "columns": {"fieldValue": "2022-06-30T14:48:39.526758"}},
                        "GroupID": {"type": "row", "columns": {"fieldValue": "0"}},
                        "trailer": {
                            "type": "collection",
                            "rows": {"CheckSum": {"type": "row", "columns": {"fieldValue": "136"}}},
                        },
                        "Side": {"type": "row", "columns": {"fieldValue": "2"}},
                        "OrdStatus": {"type": "row", "columns": {"fieldValue": "2"}},
                        "TimeInForce": {"type": "row", "columns": {"fieldValue": "0"}},
                        "SecurityID": {"type": "row", "columns": {"fieldValue": "5221001"}},
                        "ExecType": {"type": "row", "columns": {"fieldValue": "F"}},
                        "TradeLiquidityIndicator": {"type": "row", "columns": {"fieldValue": "R"}},
                        "LastLiquidityInd": {"type": "row", "columns": {"fieldValue": "2"}},
                        "LeavesQty": {"type": "row", "columns": {"fieldValue": "0"}},
                        "CumQty": {"type": "row", "columns": {"fieldValue": "20"}},
                        "LastPx": {"type": "row", "columns": {"fieldValue": "55"}},
                        "TypeOfTrade": {"type": "row", "columns": {"fieldValue": "2"}},
                        "TrdMatchID": {"type": "row", "columns": {"fieldValue": "L2N1AYTNPW"}},
                        "OrdType": {"type": "row", "columns": {"fieldValue": "2"}},
                        "ClOrdID": {"type": "row", "columns": {"fieldValue": "1985282"}},
                        "SecurityIDSource": {"type": "row", "columns": {"fieldValue": "8"}},
                        "LastMkt": {"type": "row", "columns": {"fieldValue": "XLOM"}},
                        "OrderCapacity": {"type": "row", "columns": {"fieldValue": "A"}},
                        "SecondaryClOrdID": {"type": "row", "columns": {"fieldValue": "33333"}},
                        "AccountType": {"type": "row", "columns": {"fieldValue": "1"}},
                        "Price": {"type": "row", "columns": {"fieldValue": "55"}},
                        "MDEntryID": {"type": "row", "columns": {"fieldValue": "00Amr2Sw36j1"}},
                        "TradingParty": {
                            "type": "collection",
                            "rows": {
                                "NoPartyIDs": {
                                    "type": "collection",
                                    "rows": {
                                        "0": {
                                            "type": "collection",
                                            "rows": {
                                                "PartyRole": {"type": "row", "columns": {"fieldValue": "76"}},
                                                "PartyID": {"type": "row", "columns": {"fieldValue": "ARFQ01FIX08"}},
                                                "PartyIDSource": {"type": "row", "columns": {"fieldValue": "D"}},
                                            },
                                        },
                                        "1": {
                                            "type": "collection",
                                            "rows": {
                                                "PartyRole": {"type": "row", "columns": {"fieldValue": "17"}},
                                                "PartyID": {"type": "row", "columns": {"fieldValue": "ARFQ01"}},
                                                "PartyIDSource": {"type": "row", "columns": {"fieldValue": "D"}},
                                            },
                                        },
                                        "2": {
                                            "type": "collection",
                                            "rows": {
                                                "PartyRole": {"type": "row", "columns": {"fieldValue": "3"}},
                                                "PartyID": {"type": "row", "columns": {"fieldValue": "0"}},
                                                "PartyIDSource": {"type": "row", "columns": {"fieldValue": "P"}},
                                            },
                                        },
                                        "3": {
                                            "type": "collection",
                                            "rows": {
                                                "PartyRole": {"type": "row", "columns": {"fieldValue": "122"}},
                                                "PartyID": {"type": "row", "columns": {"fieldValue": "0"}},
                                                "PartyIDSource": {"type": "row", "columns": {"fieldValue": "P"}},
                                            },
                                        },
                                        "4": {
                                            "type": "collection",
                                            "rows": {
                                                "PartyRole": {"type": "row", "columns": {"fieldValue": "12"}},
                                                "PartyID": {"type": "row", "columns": {"fieldValue": "3"}},
                                                "PartyIDSource": {"type": "row", "columns": {"fieldValue": "P"}},
                                            },
                                        },
                                    },
                                }
                            },
                        },
                        "header": {
                            "type": "collection",
                            "rows": {
                                "BeginString": {"type": "row", "columns": {"fieldValue": "FIXT.1.1"}},
                                "SenderCompID": {"type": "row", "columns": {"fieldValue": "FGW"}},
                                "SendingTime": {"type": "row", "columns": {"fieldValue": "2022-06-30T14:48:39.530311"}},
                                "TargetCompID": {"type": "row", "columns": {"fieldValue": "ARFQ01FIX08"}},
                                "ApplVerID": {"type": "row", "columns": {"fieldValue": "9"}},
                                "MsgType": {"type": "row", "columns": {"fieldValue": "8"}},
                                "MsgSeqNum": {"type": "row", "columns": {"fieldValue": "589"}},
                                "BodyLength": {"type": "row", "columns": {"fieldValue": "432"}},
                            },
                        },
                        "DisplayQty": {"type": "row", "columns": {"fieldValue": "0"}},
                    },
                }
            ],
        }
    ]
    case3 = [
        {
            "attachedEventIds": [],
            "direction": "SECOND",
            "id": "arfq01fix07:second:1656599837520228626",
            "parsedMessages": [
                {
                    "id": "arfq01fix07:second:1656599837520228626.1",
                    "match": True,
                    "message": {
                        "fields": {
                            "AccountType": {"simpleValue": "1"},
                            "ClOrdID": {"simpleValue": "1830410"},
                            "DisplayQty": {"simpleValue": "200"},
                            "OrdType": {"simpleValue": "2"},
                            "OrderCapacity": {"simpleValue": "A"},
                            "OrderQty": {"simpleValue": "200"},
                            "Price": {"simpleValue": "55"},
                            "SecondaryClOrdID": {"simpleValue": "11111"},
                            "SecurityID": {"simpleValue": "5221001"},
                            "SecurityIDSource": {"simpleValue": "8"},
                            "Side": {"simpleValue": "1"},
                            "TradingParty": {
                                "messageValue": {
                                    "fields": {
                                        "NoPartyIDs": {
                                            "listValue": {
                                                "values": [
                                                    {
                                                        "messageValue": {
                                                            "fields": {
                                                                "PartyID": {"simpleValue": "ARFQ01FIX07"},
                                                                "PartyIDSource": {"simpleValue": "D"},
                                                                "PartyRole": {"simpleValue": "76"},
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "messageValue": {
                                                            "fields": {
                                                                "PartyID": {"simpleValue": "0"},
                                                                "PartyIDSource": {"simpleValue": "P"},
                                                                "PartyRole": {"simpleValue": "3"},
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "messageValue": {
                                                            "fields": {
                                                                "PartyID": {"simpleValue": "0"},
                                                                "PartyIDSource": {"simpleValue": "P"},
                                                                "PartyRole": {"simpleValue": "122"},
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "messageValue": {
                                                            "fields": {
                                                                "PartyID": {"simpleValue": "3"},
                                                                "PartyIDSource": {"simpleValue": "P"},
                                                                "PartyRole": {"simpleValue": "12"},
                                                            }
                                                        }
                                                    },
                                                ]
                                            }
                                        }
                                    }
                                }
                            },
                            "TransactTime": {"simpleValue": "2022-06-30T14:47:59.032276"},
                            "header": {
                                "messageValue": {
                                    "fields": {
                                        "BeginString": {"simpleValue": "FIXT.1.1"},
                                        "BodyLength": {"simpleValue": "263"},
                                        "MsgSeqNum": {"simpleValue": "626"},
                                        "MsgType": {"simpleValue": "D"},
                                        "SenderCompID": {"simpleValue": "ARFQ01FIX07"},
                                        "SendingTime": {"simpleValue": "2022-06-30T14:48:24.330"},
                                        "TargetCompID": {"simpleValue": "FGW"},
                                    }
                                }
                            },
                            "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "152"}}}},
                        },
                        "metadata": {
                            "id": {
                                "connectionId": {"sessionAlias": "arfq01fix07"},
                                "direction": "SECOND",
                                "sequence": "1656599837520228626",
                                "subsequence": [1],
                            },
                            "messageType": "NewOrderSingle",
                            "protocol": "FIX",
                            "timestamp": "2022-06-30T14:48:24.422Z",
                        },
                        "parentEventId": {"id": "a4bee27b-f883-11ec-aeb3-adf8526f5eec"},
                    },
                }
            ],
            "rawMessageBase64": "OD1GSVhULjEuMQE5PTI2MwEzNT1EATM0PTYyNgE0OT1BUkZRMDFGSVgwNwE1Mj0yMDIyMDYzMC0xNDo0ODoyNC4zMzAwMDABNTY9RkdXATExPTE4MzA0MTABMjI9OAEzOD0yMDABNDA9MgE0ND01NQE0OD01MjIxMDAxATU0PTEBNjA9MjAyMjA2MzAtMTQ6NDc6NTkuMDMyMjc2ATUyNj0xMTExMQE1Mjg9QQE1ODE9MQExMTM4PTIwMAE0NTM9NAE0NDg9QVJGUTAxRklYMDcBNDQ3PUQBNDUyPTc2ATQ0OD0wATQ0Nz1QATQ1Mj0zATQ0OD0wATQ0Nz1QATQ1Mj0xMjIBNDQ4PTMBNDQ3PVABNDUyPTEyATEwPTE1MgE=",
            "sequence": "1656599837520228626",
            "sessionId": "arfq01fix07",
            "timestamp": "2022-06-30T14:48:24.422000000Z",
            "type": "message",
        }
    ]
    assert list(demo_get_messages_with_one_filter) == case3
    assert list(demo_get_messages_with_filters) == case3
    assert list(demo_get_events_with_one_filter) == case and len(case) is 1
    assert list(demo_get_events_with_filters) == case1 and len(case1) is 1
