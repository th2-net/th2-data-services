from collections import namedtuple

import pytest


@pytest.fixture
def general_data():
    data = [
        {
            "batchId": None,
            "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "[TS_1]Aggressive IOC vs two orders: second order's price is "
            "lower than first",
            "eventType": "",
            "isBatched": False,
            "parentEventId": None,
        },
        {
            "batchId": None,
            "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for "
            "instrument INSTR1",
            "eventType": "",
            "isBatched": False,
            "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
        },
        {
            "batchId": None,
            "eventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
            "eventName": 'placeOrderFIX demo-conn1 - STEP1: Trader "DEMO-CONN1" sends '
            "request to create passive Order.",
            "eventType": "placeOrderFIX",
            "isBatched": False,
            "parentEventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint",
            "eventType": "Checkpoint",
            "isBatched": True,
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a4-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'th2-hand-demo' direction 'FIRST' "
            "sequence '1623852603564709030'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a5-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn1' direction 'SECOND' "
            "sequence '1624005455622140289'",
            "eventType": "Checkpoint for session",
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a6-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'SECOND' "
            "sequence '1624005475721015014'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a7-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'FIRST' "
            "sequence '1624005475720919499'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a8-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn2' direction 'FIRST' "
            "sequence '1624005448022245399'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a9-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn2' direction 'SECOND' "
            "sequence '1624005448022426113'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114aa-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'SECOND' "
            "sequence '1624005466840347015'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ab-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'FIRST' "
            "sequence '1624005466840263372'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ac-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn1' direction 'FIRST' "
            "sequence '1624005455622011522'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ad-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-log' direction 'FIRST' "
            "sequence '1624029363623063053'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": None,
            "eventId": "8c3fec4f-d1b4-11eb-bae5-57b0c4472880",
            "eventName": "Send 'NewOrderSingle' message to connectivity",
            "eventType": "Outgoing message",
            "isBatched": False,
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        },
        {
            "batchId": None,
            "eventId": "8c44806c-d1b4-11eb-8e55-d3a76285d588",
            "eventName": "Send 'NewOrderSingle' message",
            "eventType": "Outgoing message",
            "isBatched": False,
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        },
        {
            "batchId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf",
            "eventId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf:8ca20288-d1b4-11eb-986f-1e8d42132387",
            "eventName": "Remove 'NewOrderSingle' "
            "id='demo-conn1:SECOND:1624005455622135205' "
            "Hash='7009491514226292581' Group='NOS_CONN' "
            "Hash['SecondaryClOrdID': 11111, 'SecurityID': INSTR1]",
            "isBatched": True,
            "eventType": "",
            "parentEventId": "a3779b94-d051-11eb-986f-1e8d42132387",
        },
        {
            "batchId": None,
            "eventId": "8ceb47f6-d1b4-11eb-a9ed-ffb57363e013",
            "eventName": "Send 'ExecutionReport' message",
            "isBatched": False,
            "eventType": "Send message",
            "parentEventId": "845d70d2-9c68-11eb-8598-691ebd7f413d",
        },
        {
            "batchId": None,
            "eventId": "8ced1c93-d1b4-11eb-a9f4-b12655548efc",
            "eventName": "Send 'ExecutionReport' message",
            "isBatched": False,
            "eventType": "Send message",
            "parentEventId": "845d70d2-9c68-11eb-8598-691ebd7f413d",
        },
        {
            "batchId": None,
            "eventId": "8d44d930-d1b4-11eb-bae5-57b0c4472880",
            "eventName": "Received 'ExecutionReport' response message",
            "isBatched": False,
            "eventType": "message",
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        },
        {
            "batchId": None,
            "eventId": "8d6e0c9e-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Check sequence rule SessionKey{sessionAlias='demo-conn1', "
            'direction=FIRST} - STEP2: Trader "DEMO-CONN1" receives '
            "Execution Report. The order stands on book in status NEW",
            "isBatched": False,
            "eventType": "Checkpoint for session",
            "parentEventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        },
    ]
    return data


@pytest.fixture
def test_events_tree():
    TestEventTree = namedtuple("TestEventTree", ["events", "unknown_events"])
    test_events_tree = TestEventTree(
        events=[
            "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
            "8c035903-d1b4-11eb-9278-591e568ad66e",
            "8c1114a4-d1b4-11eb-9278-591e568ad66e",
            "8c1114a5-d1b4-11eb-9278-591e568ad66e",
            "8c1114a6-d1b4-11eb-9278-591e568ad66e",
            "8c1114a7-d1b4-11eb-9278-591e568ad66e",
            "8c1114a8-d1b4-11eb-9278-591e568ad66e",
            "8c1114a9-d1b4-11eb-9278-591e568ad66e",
            "8c1114aa-d1b4-11eb-9278-591e568ad66e",
            "8c1114ab-d1b4-11eb-9278-591e568ad66e",
            "8c1114ac-d1b4-11eb-9278-591e568ad66e",
            "8c1114ad-d1b4-11eb-9278-591e568ad66e",
            "8c3fec4f-d1b4-11eb-bae5-57b0c4472880",
            "8c44806c-d1b4-11eb-8e55-d3a76285d588",
            "8ca20288-d1b4-11eb-986f-1e8d42132387",
            "8ceb47f6-d1b4-11eb-a9ed-ffb57363e013",
            "8ced1c93-d1b4-11eb-a9f4-b12655548efc",
            "8d44d930-d1b4-11eb-bae5-57b0c4472880",
            "8d6e0c9e-d1b4-11eb-9278-591e568ad66e",
        ],
        unknown_events=[
            "a3779b94-d051-11eb-986f-1e8d42132387",
            "845d70d2-9c68-11eb-8598-691ebd7f413d",
        ],
    )
    return test_events_tree


def get_super_type(record: dict, *args):
    event_type = record.get("eventType")
    if event_type:
        if not record.get("parentEventId"):
            event_type = "Test Run"
        else:
            event_type = "Test Case"

    return event_type
