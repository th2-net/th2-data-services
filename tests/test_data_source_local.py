import pytest
from urllib3.exceptions import HTTPError

from th2_data_services.data import Data
from th2_data_services.data_source import DataSource


def test_find_events_by_id_from_data_provider(demo_data_source: DataSource):
    data_source = demo_data_source

    expected_event = {
        "attachedMessageIds": [],
        "batchId": None,
        "body": {},
        "endTimestamp": {"epochSecond": 1624185888, "nano": 169710000},
        "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        "eventName": "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for " "instrument INSTR1",
        "eventType": "",
        "isBatched": False,
        "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
        "startTimestamp": {"epochSecond": 1624185888, "nano": 169672000},
        "successful": True,
        "type": "event",
    }

    expected_events = []
    expected_events.append(expected_event)
    expected_events.append(
        {
            "attachedMessageIds": [
                "demo-conn1:first:1624005455622011522",
                "demo-conn1:second:1624005455622140289",
                "demo-conn2:first:1624005448022245399",
                "demo-conn2:second:1624005448022426113",
                "demo-dc1:first:1624005475720919499",
                "demo-dc1:second:1624005475721015014",
                "demo-dc2:first:1624005466840263372",
                "demo-dc2:second:1624005466840347015",
                "demo-log:first:1624029363623063053",
                "th2-hand-demo:first:1623852603564709030",
            ],
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "body": [
                {
                    "data": "Checkpoint id '8c037f50-d1b4-11eb-ba78-1981398e00bd'",
                    "type": "message",
                }
            ],
            "endTimestamp": {"epochSecond": 1624185893, "nano": 830158000},
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint",
            "eventType": "Checkpoint",
            "isBatched": True,
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
            "startTimestamp": {"epochSecond": 1624185893, "nano": 828017000},
            "successful": True,
            "type": "event",
        }
    )

    event = data_source.find_events_by_id_from_data_provider("88a3ee80-d1b4-11eb-b0fb-199708acc7bc")
    events = data_source.find_events_by_id_from_data_provider(
        [
            "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        ]
    )
    events_with_one_element = data_source.find_events_by_id_from_data_provider(
        [
            "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        ]
    )
    for event_ in events:
        event_["attachedMessageIds"].sort()

    broken_event: dict = data_source.find_events_by_id_from_data_provider("id", True)
    broken_events: list = data_source.find_events_by_id_from_data_provider(["id", "ids"], True)
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
    assert [event, broken_event] == data_source.find_events_by_id_from_data_provider(
        ["88a3ee80-d1b4-11eb-b0fb-199708acc7bc", "id"], True
    )
    with pytest.raises(ValueError):
        data_source.find_events_by_id_from_data_provider(["88a3ee80-d1b4-11eb-b0fb-199708acc7bc", "id"])
    with pytest.raises(ValueError):
        data_source.find_events_by_id_from_data_provider("id")


def test_find_messages_by_id_from_data_provider(demo_data_source: DataSource):
    data_source = demo_data_source

    expected_message = {
        "attachedEventIds": [
            "8ea15c95-d1b4-11eb-9278-591e568ad66e",
            "8ea15c9a-d1b4-11eb-9278-591e568ad66e",
            "8d7fbfe9-d1b4-11eb-9278-591e568ad66e",
            "8d7fbfe4-d1b4-11eb-9278-591e568ad66e",
            "8c035903-d1b4-11eb-9278-591e568ad66e",
            "8c1114a8-d1b4-11eb-9278-591e568ad66e",
        ],
        "type": "message",
        "timestamp": {"nano": 123000000, "epochSecond": 1624185872},
        "direction": "IN",
        "sessionId": "demo-conn2",
        "messageType": "Heartbeat",
        "body": {
            "metadata": {
                "id": {
                    "connectionId": {"sessionAlias": "demo-conn2"},
                    "sequence": "1624005448022245399",
                    "subsequence": [1],
                },
                "timestamp": "2021-06-20T10:44:32.123Z",
                "messageType": "Heartbeat",
            },
            "fields": {
                "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "073"}}}},
                "header": {
                    "messageValue": {
                        "fields": {
                            "BeginString": {"simpleValue": "FIXT.1.1"},
                            "SenderCompID": {"simpleValue": "FGW"},
                            "SendingTime": {"simpleValue": "2021-06-20T10:44:32.122"},
                            "TargetCompID": {"simpleValue": "DEMO-CONN2"},
                            "MsgType": {"simpleValue": "0"},
                            "MsgSeqNum": {"simpleValue": "1290"},
                            "BodyLength": {"simpleValue": "59"},
                        }
                    }
                },
            },
        },
        "bodyBase64": "OD1GSVhULjEuMQE5PTU5ATM1PTABMzQ9MTI5MAE0OT1GR1cBNTI9MjAyMTA2MjAtMTA6NDQ6MzIuMTIyATU2PURFTU8tQ09OTjIBMTA9MDczAQ==",
        "messageId": "demo-conn2:first:1624005448022245399",
    }

    expected_messages = []
    expected_messages.append(expected_message)
    expected_messages.append(
        {
            "attachedEventIds": [
                "8ff68c4f-d051-11eb-9278-591e568ad66e",
                "a6401d79-d1b4-11eb-9278-591e568ad66e",
                "92a13912-d1b4-11eb-9278-591e568ad66e",
                "8f36e5b4-d051-11eb-9278-591e568ad66e",
                "e2be6278-d295-11eb-9278-591e568ad66e",
                "935ee3d3-d1b4-11eb-9278-591e568ad66e",
                "9d829081-d1b4-11eb-9278-591e568ad66e",
                "e1ece1a1-d295-11eb-9278-591e568ad66e",
                "40fd753d-d052-11eb-9278-591e568ad66e",
                "cde689e4-d295-11eb-9278-591e568ad66e",
                "ddf828a2-d295-11eb-9278-591e568ad66e",
                "e3559979-d295-11eb-9278-591e568ad66e",
                "3f9d9705-d052-11eb-9278-591e568ad66e",
                "405acc8c-d052-11eb-9278-591e568ad66e",
                "981a705c-d1b4-11eb-9278-591e568ad66e",
                "8ea15c95-d1b4-11eb-9278-591e568ad66e",
                "d93262e9-d295-11eb-9278-591e568ad66e",
                "464fe98c-d052-11eb-9278-591e568ad66e",
                "9a0f3b84-d051-11eb-9278-591e568ad66e",
                "534490a8-d052-11eb-9278-591e568ad66e",
                "cf34188b-d295-11eb-9278-591e568ad66e",
                "4e970df3-d052-11eb-9278-591e568ad66e",
                "d048e3fc-d295-11eb-9278-591e568ad66e",
                "908a8f00-d051-11eb-9278-591e568ad66e",
                "93f77b43-d051-11eb-9278-591e568ad66e",
                "de96b299-d295-11eb-9278-591e568ad66e",
                "e6b5dba0-d295-11eb-9278-591e568ad66e",
                "d47353fa-d295-11eb-9278-591e568ad66e",
                "98b3cb12-d051-11eb-9278-591e568ad66e",
                "cde662ca-d295-11eb-9278-591e568ad66e",
                "dd26f5d7-d295-11eb-9278-591e568ad66e",
                "8a1fa4c0-d051-11eb-9278-591e568ad66e",
                "d86b4248-d295-11eb-9278-591e568ad66e",
                "e3559983-d295-11eb-9278-591e568ad66e",
                "a2d776ec-d1b4-11eb-9278-591e568ad66e",
                "d86b6962-d295-11eb-9278-591e568ad66e",
                "534490b2-d052-11eb-9278-591e568ad66e",
                "9e3a95e3-d051-11eb-9278-591e568ad66e",
                "9554e885-d051-11eb-9278-591e568ad66e",
                "3b261873-d052-11eb-9278-591e568ad66e",
                "4fe475a5-d052-11eb-9278-591e568ad66e",
                "a2d776e2-d1b4-11eb-9278-591e568ad66e",
                "935ee3dd-d1b4-11eb-9278-591e568ad66e",
                "9d7968bc-d051-11eb-9278-591e568ad66e",
                "3a08735c-d052-11eb-9278-591e568ad66e",
                "981a7052-d1b4-11eb-9278-591e568ad66e",
                "45ba392b-d052-11eb-9278-591e568ad66e",
                "e6b5db96-d295-11eb-9278-591e568ad66e",
                "3c38e818-d052-11eb-9278-591e568ad66e",
                "9e3a95ed-d051-11eb-9278-591e568ad66e",
                "d9ca3634-d295-11eb-9278-591e568ad66e",
                "9ed3c8be-d051-11eb-9278-591e568ad66e",
                "9554e88f-d051-11eb-9278-591e568ad66e",
                "93ffdede-d1b4-11eb-9278-591e568ad66e",
                "d50a3ce5-d295-11eb-9278-591e568ad66e",
                "94b721d4-d051-11eb-9278-591e568ad66e",
                "405acc96-d052-11eb-9278-591e568ad66e",
                "908a67e6-d051-11eb-9278-591e568ad66e",
                "9ed3c8b4-d051-11eb-9278-591e568ad66e",
                "94b721de-d051-11eb-9278-591e568ad66e",
                "e2be6282-d295-11eb-9278-591e568ad66e",
                "a18be3f0-d1b4-11eb-9278-591e568ad66e",
                "93ffb7c4-d1b4-11eb-9278-591e568ad66e",
                "4b1b2d85-d052-11eb-9278-591e568ad66e",
                "3f9d96fb-d052-11eb-9278-591e568ad66e",
                "8ea15c9f-d1b4-11eb-9278-591e568ad66e",
                "d0490b16-d295-11eb-9278-591e568ad66e",
                "de96b2a3-d295-11eb-9278-591e568ad66e",
                "d3a79f79-d295-11eb-9278-591e568ad66e",
                "4fe4759b-d052-11eb-9278-591e568ad66e",
                "464fe996-d052-11eb-9278-591e568ad66e",
                "9c59a0da-d1b4-11eb-9278-591e568ad66e",
                "8d7fbfee-d1b4-11eb-9278-591e568ad66e",
                "8a1fa4b6-d051-11eb-9278-591e568ad66e",
                "4f443dea-d052-11eb-9278-591e568ad66e",
                "a2e77c5b-d051-11eb-9278-591e568ad66e",
                "894b8bcf-d051-11eb-9278-591e568ad66e",
                "9d82908b-d1b4-11eb-9278-591e568ad66e",
                "8b2c59e1-d051-11eb-9278-591e568ad66e",
                "ddf80188-d295-11eb-9278-591e568ad66e",
                "9d7941a2-d051-11eb-9278-591e568ad66e",
                "d4737b14-d295-11eb-9278-591e568ad66e",
                "49da7003-d052-11eb-9278-591e568ad66e",
                "44fbf334-d052-11eb-9278-591e568ad66e",
                "4a804cfa-d052-11eb-9278-591e568ad66e",
                "3b261869-d052-11eb-9278-591e568ad66e",
                "8f36e5be-d051-11eb-9278-591e568ad66e",
                "4e96e6d9-d052-11eb-9278-591e568ad66e",
                "93f77b4d-d051-11eb-9278-591e568ad66e",
                "45ba3935-d052-11eb-9278-591e568ad66e",
                "9e1337d2-d1b4-11eb-9278-591e568ad66e",
                "d93262f3-d295-11eb-9278-591e568ad66e",
                "8ff68c45-d051-11eb-9278-591e568ad66e",
                "9e1337dc-d1b4-11eb-9278-591e568ad66e",
                "9c5979c0-d1b4-11eb-9278-591e568ad66e",
                "1e67d08a-d048-11eb-986f-1e8d42132387",
                "d3a79f83-d295-11eb-9278-591e568ad66e",
                "98b3cb1c-d051-11eb-9278-591e568ad66e",
                "9a0f629e-d051-11eb-9278-591e568ad66e",
                "40fd7547-d052-11eb-9278-591e568ad66e",
                "97683741-d1b4-11eb-9278-591e568ad66e",
                "dd26f5e1-d295-11eb-9278-591e568ad66e",
                "e1ece197-d295-11eb-9278-591e568ad66e",
                "4b1b2d7b-d052-11eb-9278-591e568ad66e",
                "3a089a76-d052-11eb-9278-591e568ad66e",
                "4a807414-d052-11eb-9278-591e568ad66e",
                "cf341895-d295-11eb-9278-591e568ad66e",
                "99793d0d-d051-11eb-9278-591e568ad66e",
                "a18c0b0a-d1b4-11eb-9278-591e568ad66e",
                "a2445e9b-d1b4-11eb-9278-591e568ad66e",
                "92a1391c-d1b4-11eb-9278-591e568ad66e",
                "8c1114ad-d1b4-11eb-9278-591e568ad66e",
                "8b2c59d7-d051-11eb-9278-591e568ad66e",
                "8d7fbfe4-d1b4-11eb-9278-591e568ad66e",
                "a2e77c51-d051-11eb-9278-591e568ad66e",
                "44fbf32a-d052-11eb-9278-591e568ad66e",
                "4f446504-d052-11eb-9278-591e568ad66e",
                "894b8bc5-d051-11eb-9278-591e568ad66e",
                "3c38e80e-d052-11eb-9278-591e568ad66e",
                "8c035903-d1b4-11eb-9278-591e568ad66e",
                "9768374b-d1b4-11eb-9278-591e568ad66e",
                "49da6ff9-d052-11eb-9278-591e568ad66e",
                "997915f3-d051-11eb-9278-591e568ad66e",
                "98b41853-d1b4-11eb-9278-591e568ad66e",
                "98b4185d-d1b4-11eb-9278-591e568ad66e",
                "d9ca362a-d295-11eb-9278-591e568ad66e",
                "a6401d6f-d1b4-11eb-9278-591e568ad66e",
                "d50a3cdb-d295-11eb-9278-591e568ad66e",
                "a2445e91-d1b4-11eb-9278-591e568ad66e",
            ],
            "type": "message",
            "timestamp": {"nano": 820976000, "epochSecond": 1624029370},
            "direction": "IN",
            "sessionId": "demo-log",
            "messageType": "NewOrderSingle",
            "body": {
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "demo-log"},
                        "sequence": "1624029363623063053",
                        "subsequence": [1],
                    },
                    "timestamp": "2021-06-18T15:16:10.820976Z",
                    "messageType": "NewOrderSingle",
                },
                "fields": {
                    "OrderQty": {"simpleValue": "100"},
                    "OrdType": {"simpleValue": "2"},
                    "ClOrdID": {"simpleValue": "1687434"},
                    "SecurityIDSource": {"simpleValue": "8"},
                    "OrderCapacity": {"simpleValue": "A"},
                    "TransactTime": {"simpleValue": "2020-11-24T13:58:26.270"},
                    "SecondaryClOrdID": {"simpleValue": "33333"},
                    "AccountType": {"simpleValue": "1"},
                    "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "209"}}}},
                    "Side": {"simpleValue": "2"},
                    "Price": {"simpleValue": "34"},
                    "TimeInForce": {"simpleValue": "3"},
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
                                                        "PartyID": {"simpleValue": "DEMO-CONN2"},
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
                    "SecurityID": {"simpleValue": "INSTR2"},
                    "header": {
                        "messageValue": {
                            "fields": {
                                "BeginString": {"simpleValue": "FIXT.1.1"},
                                "SenderCompID": {"simpleValue": "DEMO-CONN2"},
                                "SendingTime": {"simpleValue": "2020-11-24T10:58:26.317"},
                                "TargetCompID": {"simpleValue": "FGW"},
                                "MsgType": {"simpleValue": "D"},
                                "MsgSeqNum": {"simpleValue": "443"},
                                "BodyLength": {"simpleValue": "250"},
                            }
                        }
                    },
                },
            },
            "bodyBase64": "OD1GSVhULjEuMQE5PTI1MAEzNT1EATM0PTQ0MwE0OT1ERU1PLUNPTk4yATUyPTIwMjAxMTI0LTEwOjU4OjI2LjMxNwE1Nj1GR1cBMTE9MTY4NzQzNAEyMj04ATM4PTEwMAE0MD0yATQ0PTM0ATQ4PUlOU1RSMgE1ND0yATU5PTMBNjA9MjAyMDExMjQtMTM6NTg6MjYuMjcwATUyNj0zMzMzMwE1Mjg9QQE1ODE9MQE0NTM9NAE0NDg9REVNTy1DT05OMgE0NDc9RAE0NTI9NzYBNDQ4PTABNDQ3PVABNDUyPTMBNDQ4PTABNDQ3PVABNDUyPTEyMgE0NDg9MwE0NDc9UAE0NTI9MTIBMTA9MjA5AQ==",
            "messageId": "demo-log:first:1624029363623063053",
        }
    )

    message = data_source.find_messages_by_id_from_data_provider("demo-conn2:first:1624005448022245399")
    messages = data_source.find_messages_by_id_from_data_provider(
        ["demo-conn2:first:1624005448022245399", "demo-log:first:1624029363623063053"]
    )
    messages_with_one_element = data_source.find_messages_by_id_from_data_provider(
        ["demo-conn2:first:1624005448022245399"]
    )
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
            "attachedMessageIds": [],
            "batchId": None,
            "body": {},
            "endTimestamp": None,
            "eventId": "f05a7c66-cdc1-11eb-b095-3f988ca527fa",
            "eventName": "[TS_0] Sending order via act-ui and verification " "ExecutionReport",
            "eventType": "",
            "isBatched": False,
            "parentEventId": None,
            "startTimestamp": {"epochSecond": 1623751840, "nano": 977716000},
            "successful": True,
            "type": "event",
        },
        {
            "attachedMessageIds": [],
            "batchId": None,
            "body": [],
            "endTimestamp": {"epochSecond": 1623751880, "nano": 978679000},
            "eventId": "08320f24-cdc2-11eb-abbf-e19b27e6e490",
            "eventName": "Send 'ExecutionReport' message",
            "eventType": "Send message",
            "isBatched": False,
            "parentEventId": "849a79d3-9c68-11eb-8598-691ebd7f413d",
            "startTimestamp": {"epochSecond": 1623751880, "nano": 978676000},
            "successful": True,
            "type": "event",
        },
        {
            "attachedMessageIds": [],
            "batchId": None,
            "body": [],
            "endTimestamp": {"epochSecond": 1623760259, "nano": 967877000},
            "eventId": "8a7650fc-cdd5-11eb-abbf-e19b27e6e490",
            "eventName": "Send 'ExecutionReport' message",
            "eventType": "Send message",
            "isBatched": False,
            "parentEventId": "849a79d3-9c68-11eb-8598-691ebd7f413d",
            "startTimestamp": {"epochSecond": 1623760259, "nano": 967873000},
            "successful": True,
            "type": "event",
        },
    ]
    case1 = [
        {
            "attachedMessageIds": [],
            "batchId": None,
            "body": [],
            "endTimestamp": {"epochSecond": 1623751880, "nano": 978679000},
            "eventId": "08320f24-cdc2-11eb-abbf-e19b27e6e490",
            "eventName": "Send 'ExecutionReport' message",
            "eventType": "Send message",
            "isBatched": False,
            "parentEventId": "849a79d3-9c68-11eb-8598-691ebd7f413d",
            "startTimestamp": {"epochSecond": 1623751880, "nano": 978676000},
            "successful": True,
            "type": "event",
        },
        {
            "attachedMessageIds": [],
            "batchId": None,
            "body": [],
            "endTimestamp": {"epochSecond": 1623760259, "nano": 967877000},
            "eventId": "8a7650fc-cdd5-11eb-abbf-e19b27e6e490",
            "eventName": "Send 'ExecutionReport' message",
            "eventType": "Send message",
            "isBatched": False,
            "parentEventId": "849a79d3-9c68-11eb-8598-691ebd7f413d",
            "startTimestamp": {"epochSecond": 1623760259, "nano": 967873000},
            "successful": True,
            "type": "event",
        },
    ]
    case3 = [
        {
            "attachedEventIds": [],
            "body": {
                "fields": {
                    "header": {
                        "messageValue": {
                            "fields": {
                                "BeginString": {"simpleValue": "FIXT.1.1"},
                                "BodyLength": {"simpleValue": "56"},
                                "MsgSeqNum": {"simpleValue": "2"},
                                "MsgType": {"simpleValue": "0"},
                                "SenderCompID": {"simpleValue": "FGW"},
                                "SendingTime": {"simpleValue": "2021-01-26T13:38:48.833"},
                                "TargetCompID": {"simpleValue": "DEMO-CONN2"},
                            }
                        }
                    },
                    "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "195"}}}},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "demo-conn2"},
                        "sequence": "1611668198530043002",
                        "subsequence": [1],
                    },
                    "messageType": "Heartbeat",
                    "timestamp": "2021-01-26T13:38:48.838Z",
                },
            },
            "bodyBase64": "OD1GSVhULjEuMQE5PTU2ATM1PTABMzQ9MgE0OT1GR1cBNTI9MjAyMTAxMjYtMTM6Mzg6NDguODMzATU2PURFTU8tQ09OTjIBMTA9MTk1AQ==",
            "direction": "IN",
            "messageId": "demo-conn2:first:1611668198530043002",
            "messageType": "Heartbeat",
            "sessionId": "demo-conn2",
            "timestamp": {"epochSecond": 1611668328, "nano": 838000000},
            "type": "message",
        },
        {
            "attachedEventIds": [],
            "body": {
                "fields": {
                    "header": {
                        "messageValue": {
                            "fields": {
                                "BeginString": {"simpleValue": "FIXT.1.1"},
                                "BodyLength": {"simpleValue": "56"},
                                "MsgSeqNum": {"simpleValue": "9"},
                                "MsgType": {"simpleValue": "0"},
                                "SenderCompID": {"simpleValue": "FGW"},
                                "SendingTime": {"simpleValue": "2021-01-26T13:42:18.834"},
                                "TargetCompID": {"simpleValue": "DEMO-CONN2"},
                            }
                        }
                    },
                    "trailer": {"messageValue": {"fields": {"CheckSum": {"simpleValue": "195"}}}},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "demo-conn2"},
                        "sequence": "1611668198530043009",
                        "subsequence": [1],
                    },
                    "messageType": "Heartbeat",
                    "timestamp": "2021-01-26T13:42:18.844Z",
                },
            },
            "bodyBase64": "OD1GSVhULjEuMQE5PTU2ATM1PTABMzQ9OQE0OT1GR1cBNTI9MjAyMTAxMjYtMTM6NDI6MTguODM0ATU2PURFTU8tQ09OTjIBMTA9MTk1AQ==",
            "direction": "IN",
            "messageId": "demo-conn2:first:1611668198530043009",
            "messageType": "Heartbeat",
            "sessionId": "demo-conn2",
            "timestamp": {"epochSecond": 1611668538, "nano": 844000000},
            "type": "message",
        },
    ]
    assert list(demo_get_messages_with_one_filter) == case3
    assert list(demo_get_messages_with_filters) == case3
    assert list(demo_get_events_with_one_filter) == case and len(case) is 3
    assert list(demo_get_events_with_filters) == case1 and len(case1) is 2


def test_find_message_by_id_from_data_provider_with_error(demo_data_source: DataSource):
    data_source = demo_data_source

    with pytest.raises(ValueError) as exc_info:
        data_source.find_messages_by_id_from_data_provider("demo-conn_not_exist:first:1624005448022245399")

    assert "Sorry, but the answer rpt-data-provider doesn't match the json format." in str(exc_info)


def test_get_events_from_data_provider_with_error(demo_data_source: DataSource):
    data_source = demo_data_source

    events = data_source.get_events_from_data_provider(startTimestamp="test", endTimestamp="test")
    with pytest.raises(HTTPError) as exc_info:
        list(events)
    assert (
        r'{"exceptionName":"java.lang.NumberFormatException","exceptionCause":"For input string: \\"test\\""}'
        in str(exc_info)
    )


def test_get_messages_from_data_provider_with_error(demo_data_source: DataSource):
    data_source = demo_data_source

    events = data_source.get_messages_from_data_provider(startTimestamp="test", endTimestamp="test", stream="test")
    with pytest.raises(HTTPError) as exc_info:
        list(events)
    assert (
        r'{"exceptionName":"java.lang.NumberFormatException","exceptionCause":"For input string: \\"test\\""}'
        in str(exc_info)
    )


def test_check_url_for_data_source():
    with pytest.raises(HTTPError) as exc_info:
        data_source = DataSource("http://test_test:8080/")
    assert "Unable to connect to host 'http://test_test:8080'\\nReason:" in str(exc_info)


def test_data_cache(demo_events_from_data_source: Data):
    data = demo_events_from_data_source
    data.use_cache(True)
    output1 = list(data)

    data.use_cache(False)
    data._data = []
    output2 = list(data)

    data.use_cache(True)
    output3 = list(data)

    output4 = list(data)

    assert output1 == output3 == output4 and output2 == []


def test_messageIds_not_in_last_msg(demo_messages_from_data_source: Data):
    data = demo_messages_from_data_source
    data_lst = list(data)
    last_msg = data_lst[-1]
    assert "messageIds" not in last_msg


def test_get_events_from_data_provider_with_metadata_true(
    demo_events_with_metadataOnly_true: Data,
    demo_events_from_data_source: Data,
    demo_events_with_metadataOnly_metadata_not_set: Data,
):
    events = list(demo_events_with_metadataOnly_true)
    events0 = list(demo_events_from_data_source)
    events1 = list(demo_events_with_metadataOnly_metadata_not_set)
    assert events == events0 == events1


def test_get_messages_from_data_provider_with_metadata_true(
    demo_messages_with_metadataOnly_true: Data,
    demo_messages_from_data_source: Data,
    demo_messages_with_metadataOnly_false: Data,
):
    messages = list(demo_messages_with_metadataOnly_true)
    messages0 = list(demo_messages_from_data_source)
    messages1 = list(demo_messages_with_metadataOnly_false)
    assert messages == messages0 == messages1


def test_get_messages_streams_many_symbols(
    demo_messages_from_data_source_with_test_streams: Data,
):
    messages = demo_messages_from_data_source_with_test_streams
    sources = messages._data.args[0]
    url1, url2 = sources[0]._data.args[0], sources[1]._data.args[0]

    assert (
        url1 == "http://10.64.66.66:30999/search/sse/messages?startTimestamp=1623750281692&endTimestamp=1623761149028"
        "&stream=Test-123&stream=Test-1234&stream=Test-12345&stream=Test-123456&stream=Test-1234567&stream"
        "=Test-12345678&stream=Test-123456789&stream=Test-1234567810&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest1&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest2&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest3&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest4&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest5&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest6&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest7&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest8&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest9&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest10&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest11&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest12&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest13&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest14&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest15&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest16&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest17&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest18&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest19"
        and url2
        == "http://10.64.66.66:30999/search/sse/messages?startTimestamp=1623750281692&endTimestamp=1623761149028"
        "&stream=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest20&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest21&stream"
        "=TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest22&stream=demo-dc1"
        "&stream=demo-dc2&stream=demo-log&stream=th2-hand-demo"
    )


def test_get_messages_with_multiple_url(
    demo_messages_from_data_source_with_test_streams: Data,
    demo_messages_from_data_source: Data,
):
    messages = demo_messages_from_data_source_with_test_streams

    messages_hand_demo_expected = demo_messages_from_data_source
    messages_hand_demo_actual = messages.filter(lambda record: record.get("sessionId") == "th2-hand-demo")

    assert len(list(messages)) == 138 and len(list(messages_hand_demo_actual)) == len(list(messages_hand_demo_expected))


def test_get_messages_with_multiple_url_double_start(
    demo_messages_from_data_source_with_test_streams: Data,
):
    messages1 = len(list(demo_messages_from_data_source_with_test_streams))
    messages2 = len(list(demo_messages_from_data_source_with_test_streams))

    assert messages1 == messages2


def test_unprintable_character(demo_data_source: DataSource):
    event = demo_data_source.find_events_by_id_from_data_provider("b85d9dca-6236-11ec-bc58-1b1c943c5c0d")

    assert "\x80" in event["body"][0]["value"] and event["body"][0]["value"] == "nobJjpBJkTuQMmscc4R\x80"
