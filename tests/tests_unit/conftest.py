import logging
import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from typing import List, NamedTuple, Sequence, Optional
import pytest
from tests.tests_unit.test_event_trees.demo_etc_data import demo_etc_data_big, demo_etc_data_small
from tests.tests_unit.utils import LogsChecker
from th2_data_services.data import Data
from th2_data_services.event_tree import EventTree, EventTreeCollection, ParentEventTreeCollection, IETCDriver
from th2_data_services.event_tree.etc_driver import Th2EventType
from th2_data_services.event_tree.exceptions import FieldIsNotExist
from th2_data_services.interfaces import IEventStruct, IEventStub

EXTERNAL_CACHE_FILE = Path().cwd() / "tests/tests_unit/test_data/test_cache/dir_for_test/external_cache_file"


@pytest.fixture
def general_data() -> List[dict]:
    """21 event."""
    data = [
        {
            "batchId": None,
            "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "[TS_1]Aggressive IOC vs two orders: second order's price is " "lower than first",
            "eventType": "",
            "isBatched": False,
            "parentEventId": None,
        },
        {
            "batchId": None,
            "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for " "instrument INSTR1",
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
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'SECOND' " "sequence '1624005475721015014'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a7-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'FIRST' " "sequence '1624005475720919499'",
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
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'SECOND' " "sequence '1624005466840347015'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ab-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'FIRST' " "sequence '1624005466840263372'",
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
            "eventName": "Checkpoint for session alias 'demo-log' direction 'FIRST' " "sequence '1624029363623063053'",
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
def detached_data() -> List[dict]:
    data = [
        {
            "batchId": None,
            "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "[TS_1]Aggressive IOC vs two orders: second order's price is " "lower than first",
            "eventType": "",
            "isBatched": False,
            "parentEventId": None,
        },
        {
            "batchId": None,
            "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for " "instrument INSTR1",
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
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'SECOND' " "sequence '1624005475721015014'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a7-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'FIRST' " "sequence '1624005475720919499'",
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
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'SECOND' " "sequence '1624005466840347015'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ab-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'FIRST' " "sequence '1624005466840263372'",
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
            "eventName": "Checkpoint for session alias 'demo-log' direction 'FIRST' " "sequence '1624029363623063053'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": None,
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
            "parentEventId": None,
        },
        {
            "batchId": None,
            "eventId": "8ceb47f6-d1b4-11eb-a9ed-ffb57363e013",
            "eventName": "Send 'ExecutionReport' message",
            "isBatched": False,
            "eventType": "Send message",
            "parentEventId": "845d70d2-9c68-11eb-8598-691ebd7f413d",
        },
    ]
    return data


@pytest.fixture
def test_events_tree() -> NamedTuple:
    TestEventTree = namedtuple("TestEventTree", ["events", "unknown_events"])
    test_events_tree = TestEventTree(
        events=[
            "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a4-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a5-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a6-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a7-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a8-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a9-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114aa-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ab-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ac-d1b4-11eb-9278-591e568ad66e",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ad-d1b4-11eb-9278-591e568ad66e",
            "8c3fec4f-d1b4-11eb-bae5-57b0c4472880",
            "8c44806c-d1b4-11eb-8e55-d3a76285d588",
            "8d44d930-d1b4-11eb-bae5-57b0c4472880",
            "8d6e0c9e-d1b4-11eb-9278-591e568ad66e",
        ],
        unknown_events=[
            "a3779b94-d051-11eb-986f-1e8d42132387",
            "845d70d2-9c68-11eb-8598-691ebd7f413d",
        ],
    )
    return test_events_tree


@pytest.fixture
def test_parent_events_tree() -> NamedTuple:
    TestEventTree = namedtuple("TestEventTree", ["events", "unknown_events"])
    test_parent_events_tree = TestEventTree(
        events=[
            "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
            "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        ],
        unknown_events=[
            "a3779b94-d051-11eb-986f-1e8d42132387",
            "845d70d2-9c68-11eb-8598-691ebd7f413d",
        ],
    )
    return test_parent_events_tree


def get_super_type(record: dict, *args):
    event_type = record.get("eventType")
    if event_type:
        if not record.get("parentEventId"):
            event_type = "Test Run"
        else:
            event_type = "Test Case"

    return event_type


@pytest.fixture
def data_for_analyzing() -> List[dict]:
    data = [
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=1, second=1),
            "type": "Test Run",
            "eventName": "test run 1",
            "successful": True,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=10, second=2),
            "type": "Heartbeat",
            "eventName": "heartbeat",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=2, second=12),
            "type": "Test Run",
            "eventName": "test run 2",
            "successful": False,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=4, second=30),
            "type": "Test Case",
            "eventName": "test case 1",
            "successful": True,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=13, second=40),
            "type": "Receive message",
            "eventName": "message123",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=2, minute=12, second=11),
            "type": "Heartbeat",
            "eventName": "heartbeat",
            "successful": False,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=2, minute=10, second=1),
            "type": "Test Case",
            "eventName": "test case 2",
            "successful": True,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=32, second=42),
            "type": "Test Case",
            "eventName": "test run 3",
            "successful": True,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=41, second=19),
            "type": "Receive message",
            "eventName": "message122",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=45, second=22),
            "type": "Verification",
            "eventName": "verification32",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=33, second=12),
            "type": "Heartbeat",
            "eventName": "heartbeat",
            "successful": False,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=1, second=59),
            "type": "Test Case",
            "eventName": "test case 3",
            "successful": False,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=3, second=54),
            "type": "Send message",
            "eventName": "message",
            "successful": False,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=54, second=52),
            "type": "Verification",
            "eventName": "verification33",
            "successful": False,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=2, minute=12, second=32),
            "type": "Send message",
            "eventName": "message123",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=2, minute=33, second=1),
            "type": "Verification",
            "eventName": "verification",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=33, second=33),
            "type": "Test Run",
            "eventName": "test run 4",
            "successful": False,
            "attachedMessageIds": False,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=44, second=44),
            "type": "Send message",
            "eventName": "message122",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=23, second=23),
            "type": "Receive message",
            "eventName": "message 333",
            "successful": False,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=55, second=55),
            "type": "Send message",
            "eventName": "message 333",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=11, second=11),
            "type": "Receive message",
            "eventName": "message 444",
            "successful": False,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=43, second=43),
            "type": "Send message",
            "eventName": "message 444",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=56, second=32),
            "type": "Receive message",
            "eventName": "message 444",
            "successful": True,
            "attachedMessageIds": True,
        },
        {
            "time": datetime(year=2021, month=1, day=1, hour=1, minute=40, second=10),
            "type": "Test Case",
            "eventName": "test case 4",
            "successful": True,
            "attachedMessageIds": False,
        },
    ]
    return data


@pytest.fixture
def general_body():
    data = {
        "rows": {
            "AccountType": {"columns": {"fieldValue": "1"}, "type": "row"},
            "ClOrdID": {"columns": {"fieldValue": "9601585"}, "type": "row"},
            "OrdType": {"columns": {"fieldValue": "2"}, "type": "row"},
            "OrderCapacity": {"columns": {"fieldValue": "A"}, "type": "row"},
            "OrderQty": {"columns": {"fieldValue": "30"}, "type": "row"},
            "Price": {"columns": {"fieldValue": "55"}, "type": "row"},
            "SecondaryClOrdID": {"columns": {"fieldValue": "11111"}, "type": "row"},
            "SecurityID": {"columns": {"fieldValue": "INSTR1"}, "type": "row"},
            "SecurityIDSource": {"columns": {"fieldValue": "8"}, "type": "row"},
            "Side": {"columns": {"fieldValue": "1"}, "type": "row"},
            "TradingParty": {
                "rows": {
                    "NoPartyIDs": {
                        "rows": {
                            "0": {
                                "rows": {
                                    "PartyID": {
                                        "columns": {"fieldValue": "DEMO-CONN1"},
                                        "type": "row",
                                    },
                                    "PartyIDSource": {
                                        "columns": {"fieldValue": "D"},
                                        "type": "row",
                                    },
                                    "PartyRole": {
                                        "columns": {"fieldValue": "76"},
                                        "type": "row",
                                    },
                                },
                                "type": "collection",
                            },
                            "1": {
                                "rows": {
                                    "PartyID": {
                                        "columns": {"fieldValue": "0"},
                                        "type": "row",
                                    },
                                    "PartyIDSource": {
                                        "columns": {"fieldValue": "P"},
                                        "type": "row",
                                    },
                                    "PartyRole": {
                                        "columns": {"fieldValue": "3"},
                                        "type": "row",
                                    },
                                },
                                "type": "collection",
                            },
                            "2": {
                                "rows": {
                                    "PartyID": {
                                        "columns": {"fieldValue": "0"},
                                        "type": "row",
                                    },
                                    "PartyIDSource": {
                                        "columns": {"fieldValue": "P"},
                                        "type": "row",
                                    },
                                    "PartyRole": {
                                        "columns": {"fieldValue": "122"},
                                        "type": "row",
                                    },
                                },
                                "type": "collection",
                            },
                            "3": {
                                "rows": {
                                    "PartyID": {
                                        "columns": {"fieldValue": "3"},
                                        "type": "row",
                                    },
                                    "PartyIDSource": {
                                        "columns": {"fieldValue": "P"},
                                        "type": "row",
                                    },
                                    "PartyRole": {
                                        "columns": {"fieldValue": "12"},
                                        "type": "row",
                                    },
                                },
                                "type": "collection",
                            },
                        },
                        "type": "collection",
                    }
                },
                "type": "collection",
            },
            "TransactTime": {
                "columns": {"fieldValue": "2021-06-20T13:44:48.170589"},
                "type": "row",
            },
        },
        "type": "treeTable",
    }
    return data


@pytest.fixture
def complex_body():
    data = [
        {
            "fields": {
                "AccountType": {
                    "actual": "1",
                    "expected": "1",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "ClOrdID": {
                    "actual": "9601585",
                    "expected": "9601585",
                    "key": True,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "CumQty": {
                    "actual": "0",
                    "expected": "0",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "ExecID": {
                    "actual": "2346",
                    "expected": "*",
                    "key": False,
                    "operation": "NOT_EMPTY",
                    "status": "PASSED",
                    "type": "field",
                },
                "ExecType": {
                    "actual": "0",
                    "expected": "0",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "LeavesQty": {
                    "actual": "30",
                    "expected": "30",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "OrdStatus": {
                    "actual": "0",
                    "expected": "0",
                    "key": True,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "OrdType": {
                    "actual": "2",
                    "expected": "2",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "OrderCapacity": {
                    "actual": "A",
                    "expected": "A",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "OrderID": {
                    "actual": "867",
                    "expected": "*",
                    "key": False,
                    "operation": "NOT_EMPTY",
                    "status": "PASSED",
                    "type": "field",
                },
                "OrderQty": {
                    "actual": "30",
                    "expected": "30",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "Price": {
                    "actual": "55",
                    "expected": "55",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "SecurityID": {
                    "actual": "INSTR1",
                    "expected": "INSTR1",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "SecurityIDSource": {
                    "actual": "8",
                    "expected": "8",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "Side": {
                    "actual": "1",
                    "expected": "1",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "PASSED",
                    "type": "field",
                },
                "Text": {
                    "actual": "Simulated New Order Buy is placed",
                    "expected": "*",
                    "key": False,
                    "operation": "NOT_EMPTY",
                    "status": "PASSED",
                    "type": "field",
                },
                "TradingParty": {
                    "actual": "1",
                    "expected": "1",
                    "fields": {
                        "NoPartyIDs": {
                            "actual": "4",
                            "expected": "4",
                            "fields": {
                                "0": {
                                    "actual": "3",
                                    "expected": "3",
                                    "fields": {
                                        "PartyID": {
                                            "actual": "DEMO-CONN1",
                                            "expected": "DEMO-CONN1",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyIDSource": {
                                            "actual": "D",
                                            "expected": "D",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyRole": {
                                            "actual": "76",
                                            "expected": "76",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                    },
                                    "key": False,
                                    "operation": "EQUAL",
                                    "type": "collection",
                                },
                                "1": {
                                    "actual": "3",
                                    "expected": "3",
                                    "fields": {
                                        "PartyID": {
                                            "actual": "0",
                                            "expected": "0",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyIDSource": {
                                            "actual": "P",
                                            "expected": "P",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyRole": {
                                            "actual": "3",
                                            "expected": "3",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                    },
                                    "key": False,
                                    "operation": "EQUAL",
                                    "type": "collection",
                                },
                                "2": {
                                    "actual": "3",
                                    "expected": "3",
                                    "fields": {
                                        "PartyID": {
                                            "actual": "0",
                                            "expected": "0",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyIDSource": {
                                            "actual": "P",
                                            "expected": "P",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyRole": {
                                            "actual": "122",
                                            "expected": "122",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                    },
                                    "key": False,
                                    "operation": "EQUAL",
                                    "type": "collection",
                                },
                                "3": {
                                    "actual": "3",
                                    "expected": "3",
                                    "fields": {
                                        "PartyID": {
                                            "actual": "3",
                                            "expected": "3",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyIDSource": {
                                            "actual": "P",
                                            "expected": "P",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                        "PartyRole": {
                                            "actual": "12",
                                            "expected": "12",
                                            "key": False,
                                            "operation": "EQUAL",
                                            "status": "PASSED",
                                            "type": "field",
                                        },
                                    },
                                    "key": False,
                                    "operation": "EQUAL",
                                    "type": "collection",
                                },
                            },
                            "key": False,
                            "operation": "EQUAL",
                            "type": "collection",
                        }
                    },
                    "key": False,
                    "operation": "EQUAL",
                    "type": "collection",
                },
                "TransactTime": {
                    "actual": "2021-06-20T10:44:55",
                    "expected": "null",
                    "key": False,
                    "operation": "EQUAL",
                    "status": "NA",
                    "type": "field",
                },
                "header": {
                    "actual": "7",
                    "expected": "7",
                    "fields": {
                        "BeginString": {
                            "actual": "FIXT.1.1",
                            "expected": "FIXT.1.1",
                            "key": False,
                            "operation": "EQUAL",
                            "status": "PASSED",
                            "type": "field",
                        },
                        "BodyLength": {
                            "actual": "310",
                            "expected": "*",
                            "key": False,
                            "operation": "NOT_EMPTY",
                            "status": "PASSED",
                            "type": "field",
                        },
                        "MsgSeqNum": {
                            "actual": "1291",
                            "expected": "*",
                            "key": False,
                            "operation": "NOT_EMPTY",
                            "status": "PASSED",
                            "type": "field",
                        },
                        "MsgType": {
                            "actual": "8",
                            "expected": "8",
                            "key": False,
                            "operation": "EQUAL",
                            "status": "PASSED",
                            "type": "field",
                        },
                        "SenderCompID": {
                            "actual": "FGW",
                            "expected": "*",
                            "key": False,
                            "operation": "NOT_EMPTY",
                            "status": "PASSED",
                            "type": "field",
                        },
                        "SendingTime": {
                            "actual": "2021-06-20T10:44:55.346",
                            "expected": "*",
                            "key": False,
                            "operation": "NOT_EMPTY",
                            "status": "PASSED",
                            "type": "field",
                        },
                        "TargetCompID": {
                            "actual": "DEMO-CONN1",
                            "expected": "DEMO-CONN1",
                            "key": False,
                            "operation": "EQUAL",
                            "status": "PASSED",
                            "type": "field",
                        },
                    },
                    "key": False,
                    "operation": "EQUAL",
                    "type": "collection",
                },
                "trailer": {
                    "actual": "1",
                    "expected": "null",
                    "fields": {
                        "CheckSum": {
                            "actual": "056",
                            "expected": "null",
                            "key": False,
                            "operation": "EQUAL",
                            "status": "NA",
                            "type": "field",
                        }
                    },
                    "key": False,
                    "operation": "EQUAL",
                    "status": "NA",
                    "type": "collection",
                },
            },
            "type": "verification",
        }
    ]

    return data


@pytest.fixture
def messages_before_pipeline_adapter():
    messages = [
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce"],
            "body": {
                "fields": {
                    "PHCount": {"simpleValue": "0"},
                    "PHSequence": {"simpleValue": "15499"},
                    "PHSession": {"simpleValue": "M127205328"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617064",
                        "subsequence": [1],
                    },
                    "messageType": "PacketHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:37.928Z",
                },
            },
            "bodyBase64": "TTEyNzIwNTMyOAAAAAAAADyLAAA=",
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617064",
            "messageType": "PacketHeader",
            "sessionId": "test-42",
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "TestMessageHeader": {"messageValue": {"fields": {"Length": {"simpleValue": "4"}}}},
                    "PacketHeader": {
                        "messageValue": {
                            "fields": {
                                "PHCount": {"simpleValue": "3"},
                                "PHSequence": {"simpleValue": "15487"},
                                "PHSession": {"simpleValue": "M127204538"},
                            }
                        }
                    },
                    "SecondsMessage": {
                        "messageValue": {
                            "fields": {
                                "MessageSequenceNumber": {"simpleValue": "15487"},
                                "MessageType": {"simpleValue": "T"},
                                "PHCount": {"simpleValue": "3"},
                                "PHSequence": {"simpleValue": "15487"},
                                "PHSession": {"simpleValue": "M127204538"},
                                "Second": {"simpleValue": "1632375458"},
                            }
                        }
                    },
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216519834417326",
                        "subsequence": [1, 2, 3],
                    },
                    "messageType": "PacketHeader/TestMessageHeader/SecondsMessage",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216519834417326",
            "messageType": "PacketHeader/TestMessageHeader/SecondsMessage/TestMessageHeader/AddOrder",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "AddOrder-5": {
                        "messageValue": {
                            "fields": {
                                "ExchangeOrderType": {"simpleValue": "0"},
                                "LotType": {"simpleValue": "2"},
                                "MessageSequenceNumber": {"simpleValue": "15500"},
                                "MessageType": {"simpleValue": "A"},
                                "OrderBookID": {"simpleValue": "119549"},
                                "OrderBookPosition": {"simpleValue": "1"},
                                "OrderID": {"simpleValue": "7478143635544868134"},
                                "PHCount": {"simpleValue": "2"},
                                "PHSequence": {"simpleValue": "15499"},
                                "PHSession": {"simpleValue": "M127205328"},
                                "Price": {"simpleValue": "1000"},
                                "Quantity": {"simpleValue": "2000"},
                                "Side": {"simpleValue": "B"},
                                "TimestampNanoseconds": {"simpleValue": "2724576"},
                            }
                        }
                    },
                    "TestMessageHeader-2": {"messageValue": {"fields": {"Length": {"simpleValue": "5"}}}},
                    "TestMessageHeader-4": {"messageValue": {"fields": {"Length": {"simpleValue": "37"}}}},
                    "PacketHeader-1": {
                        "messageValue": {
                            "fields": {
                                "PHCount": {"simpleValue": "2"},
                                "PHSequence": {"simpleValue": "15499"},
                                "PHSession": {"simpleValue": "M127205328"},
                            }
                        }
                    },
                    "SecondsMessage-3": {
                        "messageValue": {
                            "fields": {
                                "MessageSequenceNumber": {"simpleValue": "15499"},
                                "MessageType": {"simpleValue": "T"},
                                "PHCount": {"simpleValue": "2"},
                                "PHSequence": {"simpleValue": "15499"},
                                "PHSession": {"simpleValue": "M127205328"},
                                "Second": {"simpleValue": "1632375458"},
                            }
                        }
                    },
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617066",
                        "subsequence": [1, 2, 3, 4, 5],
                    },
                    "messageType": "PacketHeader/TestMessageHeader/SecondsMessage/TestMessageHeader/AddOrder",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617066",
            "messageType": "PacketHeader/TestMessageHeader/SecondsMessage/TestMessageHeader/AddOrder",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce"],
            "body": {
                "fields": {
                    "MessageSequenceNumber": {"simpleValue": "15239"},
                    "MessageType": {"simpleValue": "T"},
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "154319"},
                    "PHSession": {"simpleValue": "M1212305328"},
                    "Second": {"simpleValue": "163231325458"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617064",
                        "subsequence": [1],
                    },
                    "messageType": "SecondsMessage",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:37.928Z",
                },
            },
            "bodyBase64": "TTEyNLOeedaNTMyOAPPPPPFyLuAA=",
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617064",
            "messageType": "SecondsMessage",
            "sessionId": "test-42",
            "type": "message",
        },
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce"],
            "body": {
                "fields": {
                    "ExchangeOrderType": {"simpleValue": "0"},
                    "LotType": {"simpleValue": "2"},
                    "MessageSequenceNumber": {"simpleValue": "15330"},
                    "MessageType": {"simpleValue": "A"},
                    "OrderBookID": {"simpleValue": "133549"},
                    "OrderBookPosition": {"simpleValue": "1"},
                    "OrderID": {"simpleValue": "7478143635544868134"},
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "13399"},
                    "PHSession": {"simpleValue": "M127205328"},
                    "Price": {"simpleValue": "1330"},
                    "Quantity": {"simpleValue": "2200"},
                    "Side": {"simpleValue": "B"},
                    "TimestampNanoseconds": {"simpleValue": "2724576"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617064",
                        "subsequence": [1],
                    },
                    "messageType": "AddOrder",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:37.928Z",
                },
            },
            "bodyBase64": "ppEDEyNzIwPPPEDAOAAAAAAAADyLAAA=",
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617064",
            "messageType": "AddOrder",
            "sessionId": "test-42",
            "type": "message",
        },
    ]
    return messages


@pytest.fixture
def messages_after_pipeline_adapter():
    messages = [
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce"],
            "body": {
                "fields": {
                    "PHCount": {"simpleValue": "0"},
                    "PHSequence": {"simpleValue": "15499"},
                    "PHSession": {"simpleValue": "M127205328"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617064",
                        "subsequence": [1],
                    },
                    "messageType": "PacketHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:37.928Z",
                },
            },
            "bodyBase64": "TTEyNzIwNTMyOAAAAAAAADyLAAA=",
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617064",
            "messageType": "PacketHeader",
            "sessionId": "test-42",
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {"Length": {"simpleValue": "4"}},
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216519834417326",
                        "subsequence": [2],
                    },
                    "messageType": "TestMessageHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216519834417326.2",
            "messageType": "TestMessageHeader",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "PHCount": {"simpleValue": "3"},
                    "PHSequence": {"simpleValue": "15487"},
                    "PHSession": {"simpleValue": "M127204538"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216519834417326",
                        "subsequence": [1],
                    },
                    "messageType": "PacketHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216519834417326.1",
            "messageType": "PacketHeader",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "MessageSequenceNumber": {"simpleValue": "15487"},
                    "MessageType": {"simpleValue": "T"},
                    "PHCount": {"simpleValue": "3"},
                    "PHSequence": {"simpleValue": "15487"},
                    "PHSession": {"simpleValue": "M127204538"},
                    "Second": {"simpleValue": "1632375458"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216519834417326",
                        "subsequence": [3],
                    },
                    "messageType": "SecondsMessage",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216519834417326.3",
            "messageType": "SecondsMessage",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "ExchangeOrderType": {"simpleValue": "0"},
                    "LotType": {"simpleValue": "2"},
                    "MessageSequenceNumber": {"simpleValue": "15500"},
                    "MessageType": {"simpleValue": "A"},
                    "OrderBookID": {"simpleValue": "119549"},
                    "OrderBookPosition": {"simpleValue": "1"},
                    "OrderID": {"simpleValue": "7478143635544868134"},
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "15499"},
                    "PHSession": {"simpleValue": "M127205328"},
                    "Price": {"simpleValue": "1000"},
                    "Quantity": {"simpleValue": "2000"},
                    "Side": {"simpleValue": "B"},
                    "TimestampNanoseconds": {"simpleValue": "2724576"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617066",
                        "subsequence": [5],
                    },
                    "messageType": "AddOrder",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617066.5",
            "messageType": "AddOrder",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {"Length": {"simpleValue": "5"}},
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617066",
                        "subsequence": [2],
                    },
                    "messageType": "TestMessageHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617066.2",
            "messageType": "TestMessageHeader",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {"Length": {"simpleValue": "37"}},
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617066",
                        "subsequence": [4],
                    },
                    "messageType": "TestMessageHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617066.4",
            "messageType": "TestMessageHeader",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "15499"},
                    "PHSession": {"simpleValue": "M127205328"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617066",
                        "subsequence": [1],
                    },
                    "messageType": "PacketHeader",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617066.1",
            "messageType": "PacketHeader",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": [
                "09960e51-1c6b-11ec-9d85-cd5454918fce",
                "09963563-1c6b-11ec-9d85-cd5454918fce",
            ],
            "body": {
                "fields": {
                    "MessageSequenceNumber": {"simpleValue": "15499"},
                    "MessageType": {"simpleValue": "T"},
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "15499"},
                    "PHSession": {"simpleValue": "M127205328"},
                    "Second": {"simpleValue": "1632375458"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617066",
                        "subsequence": [3],
                    },
                    "messageType": "SecondsMessage",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:38.004Z",
                },
            },
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617066.3",
            "messageType": "SecondsMessage",
            "sessionId": "test-42",
            "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
            "type": "message",
        },
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce"],
            "body": {
                "fields": {
                    "MessageSequenceNumber": {"simpleValue": "15239"},
                    "MessageType": {"simpleValue": "T"},
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "154319"},
                    "PHSession": {"simpleValue": "M1212305328"},
                    "Second": {"simpleValue": "163231325458"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617064",
                        "subsequence": [1],
                    },
                    "messageType": "SecondsMessage",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:37.928Z",
                },
            },
            "bodyBase64": "TTEyNLOeedaNTMyOAPPPPPFyLuAA=",
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617064",
            "messageType": "SecondsMessage",
            "sessionId": "test-42",
            "type": "message",
        },
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce"],
            "body": {
                "fields": {
                    "ExchangeOrderType": {"simpleValue": "0"},
                    "LotType": {"simpleValue": "2"},
                    "MessageSequenceNumber": {"simpleValue": "15330"},
                    "MessageType": {"simpleValue": "A"},
                    "OrderBookID": {"simpleValue": "133549"},
                    "OrderBookPosition": {"simpleValue": "1"},
                    "OrderID": {"simpleValue": "7478143635544868134"},
                    "PHCount": {"simpleValue": "2"},
                    "PHSequence": {"simpleValue": "13399"},
                    "PHSession": {"simpleValue": "M127205328"},
                    "Price": {"simpleValue": "1330"},
                    "Quantity": {"simpleValue": "2200"},
                    "Side": {"simpleValue": "B"},
                    "TimestampNanoseconds": {"simpleValue": "2724576"},
                },
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "test-42"},
                        "sequence": "1632216515838617064",
                        "subsequence": [1],
                    },
                    "messageType": "AddOrder",
                    "protocol": "SOUP",
                    "timestamp": "2021-09-23T12:37:37.928Z",
                },
            },
            "bodyBase64": "ppEDEyNzIwPPPEDAOAAAAAAAADyLAAA=",
            "direction": "IN",
            "messageId": "test-42:first:1632216515838617064",
            "messageType": "AddOrder",
            "sessionId": "test-42",
            "type": "message",
        },
    ]
    return messages


@pytest.fixture
def message_from_pipeline():
    message = {
        "attachedEventIds": [
            "09960e51-1c6b-11ec-9d85-cd5454918fce",
            "09963563-1c6b-11ec-9d85-cd5454918fce",
        ],
        "body": {
            "fields": {
                "AddOrder-5": {
                    "messageValue": {
                        "fields": {
                            "ExchangeOrderType": {"simpleValue": "0"},
                            "LotType": {"simpleValue": "2"},
                            "MessageSequenceNumber": {"simpleValue": "15500"},
                            "MessageType": {"simpleValue": "A"},
                            "OrderBookID": {"simpleValue": "119549"},
                            "OrderBookPosition": {"simpleValue": "1"},
                            "OrderID": {"simpleValue": "7478143635544868134"},
                            "PHCount": {"simpleValue": "2"},
                            "PHSequence": {"simpleValue": "15499"},
                            "PHSession": {"simpleValue": "M127205328"},
                            "Price": {"simpleValue": "1000"},
                            "Quantity": {"simpleValue": "2000"},
                            "Side": {"simpleValue": "B"},
                            "TimestampNanoseconds": {"simpleValue": "2724576"},
                        }
                    }
                },
                "TestMessageHeader-2": {"messageValue": {"fields": {"Length": {"simpleValue": "5"}}}},
                "TestMessageHeader-4": {"messageValue": {"fields": {"Length": {"simpleValue": "37"}}}},
                "PacketHeader-1": {
                    "messageValue": {
                        "fields": {
                            "PHCount": {"simpleValue": "2"},
                            "PHSequence": {"simpleValue": "15499"},
                            "PHSession": {"simpleValue": "M127205328"},
                        }
                    }
                },
                "SecondsMessage-3": {
                    "messageValue": {
                        "fields": {
                            "MessageSequenceNumber": {"simpleValue": "15499"},
                            "MessageType": {"simpleValue": "T"},
                            "PHCount": {"simpleValue": "2"},
                            "PHSequence": {"simpleValue": "15499"},
                            "PHSession": {"simpleValue": "M127205328"},
                            "Second": {"simpleValue": "1632375458"},
                        }
                    }
                },
            },
            "metadata": {
                "id": {
                    "connectionId": {"sessionAlias": "test-42"},
                    "sequence": "1632216515838617066",
                    "subsequence": [1, 2, 3, 4, 5],
                },
                "messageType": "PacketHeader/TestMessageHeader/SecondsMessage/TestMessageHeader/AddOrder",
                "protocol": "SOUP",
                "timestamp": "2021-09-23T12:37:38.004Z",
            },
        },
        "direction": "IN",
        "messageId": "test-42:first:1632216515838617066",
        "messageType": "PacketHeader/TestMessageHeader/SecondsMessage/TestMessageHeader/AddOrder",
        "sessionId": "test-42",
        "timestamp": {"epochSecond": 1632400658, "nano": 4000000},
        "type": "message",
    }
    return message


@pytest.fixture
def message_from_pipeline_empty_body():
    messages = {
        "attachedEventIds": [],
        "body": {
            "fields": {
                "Csv_Header": {"fields": {}, "metadata": {}},
                "Csv_Message": {
                    "fields": {},
                    "metadata": {
                        "TestField": "test",
                        "timestamp": "2021-10-12T12:13:59.766600545Z",
                    },
                },
            },
            "metadata": {
                "id": {
                    "connectionId": {"sessionAlias": "satscomments2"},
                    "sequence": "1634314921633704398",
                    "subsequence": [1],
                },
                "messageType": "Csv_Header",
                "properties": {"logTimestamp": "2021-10-12 " "12:13:59.733300545"},
                "timestamp": "2021-10-12T12:13:59.733300545Z",
            },
        },
        "bodyBase64": "Ik1lc3NhZ2UiLCJNc2dUeXBlIgoiQU8xMjExMDEyMTIwOTA3MTE0MDAxIC0gZGVwdGggeWllbGRzIG5vIGJhdGNoIiwiU0FUU0NvbW1lbnRzIg==",
        "direction": "IN",
        "messageId": "satscomments2:first:1634314921633704398",
        "messageType": "Csv_Header/Csv_Message",
        "sessionId": "satscomments2",
        "timestamp": {"epochSecond": 1634040839, "nano": 733300545},
        "type": "message",
    }
    return messages


@pytest.fixture
def messages_from_after_pipeline_empty_body():
    messages = [
        {
            "attachedEventIds": [],
            "body": {
                "fields": {},
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "satscomments2"},
                        "sequence": "1634314921633704398",
                        "subsequence": [1],
                    },
                    "messageType": "Csv_Header",
                    "properties": {"logTimestamp": "2021-10-12 " "12:13:59.733300545"},
                    "timestamp": "2021-10-12T12:13:59.733300545Z",
                },
            },
            "bodyBase64": "Ik1lc3NhZ2UiLCJNc2dUeXBlIgoiQU8xMjExMDEyMTIwOTA3MTE0MDAxIC0gZGVwdGggeWllbGRzIG5vIGJhdGNoIiwiU0FUU0NvbW1lbnRzIg==",
            "direction": "IN",
            "messageId": "satscomments2:first:1634314921633704398.1",
            "messageType": "Csv_Header",
            "sessionId": "satscomments2",
            "timestamp": {"epochSecond": 1634040839, "nano": 733300545},
            "type": "message",
        },
        {
            "attachedEventIds": [],
            "body": {
                "fields": {},
                "metadata": {
                    "id": {
                        "connectionId": {"sessionAlias": "satscomments2"},
                        "sequence": "1634314921633704398",
                        "subsequence": [2],
                    },
                    "messageType": "Csv_Message",
                    "properties": {"logTimestamp": "2021-10-12 " "12:13:59.733300545"},
                    "timestamp": "2021-10-12T12:13:59.766600545Z",
                    "TestField": "test",
                },
            },
            "bodyBase64": "Ik1lc3NhZ2UiLCJNc2dUeXBlIgoiQU8xMjExMDEyMTIwOTA3MTE0MDAxIC0gZGVwdGggeWllbGRzIG5vIGJhdGNoIiwiU0FUU0NvbW1lbnRzIg==",
            "direction": "IN",
            "messageId": "satscomments2:first:1634314921633704398.2",
            "messageType": "Csv_Message",
            "sessionId": "satscomments2",
            "timestamp": {"epochSecond": 1634040839, "nano": 733300545},
            "type": "message",
        },
    ]
    return messages


@pytest.fixture(params=[True, False])
def cache(request):
    return request.param


@pytest.fixture
def log_checker(caplog) -> LogsChecker:
    """Activates DS lib logging and returns Log checker class."""
    caplog.set_level(logging.DEBUG, logger="th2_data_services")
    return LogsChecker(caplog)


@pytest.fixture
def parentless_data() -> List[dict]:
    data = [
        {"type": "event", "eventId": "a", "eventName": "a", "parentEventId": None},
        {"type": "event", "eventId": "b", "eventName": "b", "parentEventId": "a"},
        {"type": "event", "eventId": "c", "eventName": "c", "parentEventId": "b"},
        {"type": "event", "eventId": "x", "eventName": "x", "parentEventId": None},
        {"type": "event", "eventId": "y", "eventName": "y", "parentEventId": "x"},
        {"type": "event", "eventId": "z", "eventName": "z", "parentEventId": "y"},
        {"type": "event", "eventId": "d", "eventName": "d", "parentEventId": "e"},
        {"type": "event", "eventId": "t", "eventName": "t", "parentEventId": "d"},
    ]
    return data


@pytest.fixture(params=[True, False])
def interactive_mod(request):
    """INTERACTIVE_MODE or script mod"""
    INTERACTIVE_MODE = request.param
    return INTERACTIVE_MODE


DataCase = namedtuple("DataCase", ["data", "create_type", "expected_data_values"])

case1_values = ["a", "b", "c", "d", "e", "f", "g"]


# TODO - make data_case with the same set of data maybe?
@pytest.fixture(
    params=[
        DataCase(Data(case1_values, cache=True), "list", case1_values),
        DataCase(Data.from_cache_file(EXTERNAL_CACHE_FILE), "external_cache_file", general_data),
        DataCase(Data([1, 2, 3]) + Data([4, 5, 6, "end", {"a": 123}]), "join", [1, 2, 3, 4, 5, 6, "end", {"a": 123}]),
    ]
)
def data_case(request) -> DataCase:
    """
    Possible Data objects

    STR_PRINT_LEN = 5

    1. Init with list
    1.1. With <= STR_PRINT_LEN args
    1.2. With > STR_PRINT_LEN args

    2. Init with joining
    2.1. With <= STR_PRINT_LEN args
    2.2. With > STR_PRINT_LEN args

    3. Init with external cache file


    """
    return request.param


@pytest.fixture
def tmp_test_folder() -> Path:
    """."""
    cwd = Path.cwd().resolve()
    new_dir = cwd / "test_dir"
    new_dir.mkdir(exist_ok=True)
    yield new_dir
    os.chdir(cwd)


@pytest.fixture
def events_tree_for_test() -> EventTree:
    tree = EventTree(event_name="root event", event_id="root_id", data={"data": [1, 2, 3, 4, 5]})
    tree.append_event(event_name="A", event_id="A_id", data=None, parent_id="root_id")
    tree.append_event(event_name="B", event_id="B_id", data=None, parent_id="root_id")
    tree.append_event(event_name="C", event_id="C_id", data={"data": "test data"}, parent_id="B_id")
    tree.append_event(event_name="D", event_id="D_id", data=None, parent_id="B_id")
    tree.append_event(event_name="D1", event_id="D1_id", data={"key1": "value1", "key2": "value2"}, parent_id="D_id")
    return tree


class DemoEventStruct(IEventStruct):
    EVENT_ID = "eventId"
    PARENT_EVENT_ID = "parentEventId"
    STATUS = "successful"
    NAME = "eventName"
    BATCH_ID = "batchId"
    IS_BATCHED = "isBatched"
    EVENT_TYPE = "eventType"
    END_TIMESTAMP = "endTimestamp"
    START_TIMESTAMP = "startTimestamp"
    ATTACHED_MESSAGES_IDS = "attachedMessageIds"
    BODY = "body"


class DemoEventStubBuilder(IEventStub):
    def __init__(self, event_struct):
        self.event_fields = event_struct
        super().__init__()  # Requirement to define fields for the template earlier.

    @property
    def template(self) -> dict:
        return {
            self.event_fields.ATTACHED_MESSAGES_IDS: [],
            self.event_fields.BATCH_ID: "Broken_Event",
            self.event_fields.END_TIMESTAMP: {"nano": 0, "epochSecond": 0},
            self.event_fields.START_TIMESTAMP: {"nano": 0, "epochSecond": 0},
            self.event_fields.EVENT_ID: self.REQUIRED_FIELD,
            self.event_fields.NAME: "Broken_Event",
            self.event_fields.EVENT_TYPE: "Broken_Event",
            self.event_fields.PARENT_EVENT_ID: "Broken_Event",
            self.event_fields.STATUS: None,
            self.event_fields.IS_BATCHED: None,
        }


class DemoDriver(IETCDriver):
    def __init__(
        self,
        data_source=None,
        event_struct=DemoEventStruct(),
        use_stub: bool = False,
    ):
        super().__init__(data_source=data_source, event_struct=event_struct, use_stub=use_stub)
        self.stub_builder = DemoEventStubBuilder(event_struct)

    def get_event_id(self, event: Th2EventType) -> str:
        try:
            if event:
                return event[self.event_struct.EVENT_ID]
        except KeyError:
            raise FieldIsNotExist(self.event_struct.EVENT_ID)

    def get_event_name(self, event: Th2EventType) -> str:
        try:
            if event:
                return event[self.event_struct.NAME]
        except KeyError:
            raise FieldIsNotExist(self.event_struct.NAME)

    def get_parent_event_id(self, event) -> Optional[str]:
        return event.get(self.event_struct.PARENT_EVENT_ID)

    def get_events_by_id_from_source(self, ids: Sequence) -> list:
        ...

    def build_stub_event(self, id_):
        return self.stub_builder.build({self.event_struct.EVENT_ID: id_})

    def stub_event_name(self):
        return self.stub_builder.template[self.event_struct.NAME]


@pytest.fixture
def demo_etc_driver():
    return DemoDriver()


@pytest.fixture
def demo_etc(demo_etc_driver):
    data = Data(demo_etc_data_small)
    etc = EventTreeCollection(demo_etc_driver)
    etc.build(data)
    return etc


@pytest.fixture
def demo_etc_with_general_data(demo_etc_driver, general_data):
    data = Data(general_data)
    etc = EventTreeCollection(demo_etc_driver)
    etc.build(data)
    return etc


@pytest.fixture
def demo_petc(demo_etc_driver):
    data = Data(demo_etc_data_small)
    etc = ParentEventTreeCollection(demo_etc_driver)
    etc.build(data)
    return etc


@pytest.fixture
def demo_petc_with_general_data(demo_etc_driver, general_data):
    data = Data(general_data)
    petc = ParentEventTreeCollection(demo_etc_driver)
    petc.build(data)
    return petc


@pytest.fixture
def demo_etc_big(demo_etc_driver) -> EventTreeCollection:
    data = Data(demo_etc_data_big)
    etc = EventTreeCollection(demo_etc_driver)
    etc.build(data)
    return etc


@pytest.fixture
def frequency_table_data():
    data = [
        ['2023-08-14T08:53:05.688049Z', 'OrderCancel', 'OUT', 'stream2'],
        ['2023-08-21T07:51:27.942076Z', 'NewOrder', 'IN', 'stream4'],
        ['2023-08-24T11:51:12.616085Z', 'NewOrder', 'IN', 'stream1'],
        ['2023-08-16T05:41:54.963540Z', 'OrderCancel', 'OUT', 'stream2'],
        ['2023-08-16T15:29:01.422646Z', 'NewOrder', 'IN', 'stream4'],
        ['2023-08-19T02:49:16.551326Z', 'NewOrder', 'OUT', 'stream1'],
        ['2023-08-22T23:06:20.612952Z', 'ExecutionReport', 'OUT', 'stream3'],
        ['2023-08-23T20:12:40.152099Z', 'NewOrder', 'OUT', 'stream1'],
        ['2023-08-16T02:15:49.844689Z', 'OrderCancel', 'OUT', 'stream2'],
        ['2023-08-23T11:16:11.021005Z', 'NewOrder', 'OUT', 'stream1'],
        ['2023-08-21T09:15:39.315806Z', 'ExecutionReport', 'OUT', 'stream3'],
        ['2023-08-21T23:27:37.341876Z', 'NewOrder', 'OUT', 'stream1'],
        ['2023-08-14T13:49:10.534961Z', 'OrderCancel', 'IN', 'stream2'],
        ['2023-08-16T23:07:22.431359Z', 'OrderCancel', 'IN', 'stream3'],
        ['2023-08-24T04:35:55.852704Z', 'NewOrder', 'OUT', 'stream4'],
        ['2023-08-20T10:31:42.493202Z', 'OrderCancel', 'OUT', 'stream2'],
        ['2023-08-13T18:45:42.299591Z', 'OrderCancel', 'OUT', 'stream2'],
        ['2023-08-20T07:51:16.455842Z', 'OrderCancel', 'OUT', 'stream4'],
        ['2023-08-14T22:23:47.334876Z', 'NewOrder', 'IN', 'stream4'],
        ['2023-08-23T11:13:21.811535Z', 'NewOrder', 'IN', 'stream2'],
        ['2023-08-13T21:34:04.089095Z', 'NewOrder', 'OUT', 'stream4'],
        ['2023-08-14T19:53:49.159667Z', 'ExecutionReport', 'IN', 'stream1'],
        ['2023-08-13T17:23:15.927140Z', 'ExecutionReport', 'OUT', 'stream1'],
        ['2023-08-19T21:06:32.548659Z', 'ExecutionReport', 'IN', 'stream3'],
        ['2023-08-16T06:26:01.182164Z', 'NewOrder', 'OUT', 'stream2'],
        ['2023-08-21T23:19:27.914964Z', 'NewOrder', 'IN', 'stream3'],
        ['2023-08-17T12:13:45.597220Z', 'ExecutionReport', 'OUT', 'stream2'],
        ['2023-08-24T04:10:05.793870Z', 'OrderCancel', 'IN', 'stream1'],
        ['2023-08-17T10:25:05.916986Z', 'OrderCancel', 'IN', 'stream2'],
        ['2023-08-13T19:38:00.721701Z', 'OrderCancel', 'IN', 'stream3'],
    ]
    return data