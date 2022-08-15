from datetime import datetime

import pytest
import requests

from th2_data_services.data import Data
from th2_data_services.provider.exceptions import CommandError
from th2_data_services.provider.v5.commands.http import GetEvents, GetMessages
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.commands import http


def test_find_events_by_id_from_data_provider(demo_data_source: HTTPProvider5DataSource):
    data_source = demo_data_source

    expected_event = {
        'attachedMessageIds': [],
        'batchId': None,
        'body': {},
        'endTimestamp': {'epochSecond': 1656599851, 'nano': 420806000},
        'eventId': '2c4b3a58-f882-11ec-b952-0a1e730db2c6',
        'eventName': 'Recon: Test',
        'eventType': '',
        'isBatched': False,
        'parentEventId': None,
        'startTimestamp': {'epochSecond': 1656599851, 'nano': 420806000},
        'successful': False,
        'type': 'event'
    }

    expected_events = []
    expected_events.append(expected_event)
    expected_events.append(
        {'type': 'event', 'eventId': 'a5586d90-b83b-48a4-bd2b-b2059fb79374:b84cff2c-f883-11ec-b070-0a1e730db2c6',
         'batchId': 'a5586d90-b83b-48a4-bd2b-b2059fb79374', 'isBatched': True,
         'eventName': "Match by ClOrdID: '7706360'", 'eventType': '',
         'endTimestamp': {'nano': 809998000, 'epochSecond': 1656600515},
         'startTimestamp': {'nano': 809998000, 'epochSecond': 1656600515},
         'parentEventId': 'b21a03c0-f883-11ec-b070-0a1e730db2c6', 'successful': True,
         'attachedMessageIds': ['arfq01fix08:first:1656599887515453583', 'arfq01fix08:second:1656599887515499581'],
         'body': {'type': 'table', 'rows': [{'Name': 'ClOrdId', 'Value': '7706360'},
                                            {'Name': 'Message Response', 'Value': 'ExecutionReport'},
                                            {'Name': 'Message Request', 'Value': 'NewOrderSingle'},
                                            {'Name': 'Latency type', 'Value': 'Trade'},
                                            {'Name': 'Latency', 'Value': 29000.0}],
                  '_TableComponent__column_names': ['Name', 'Value']}}
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


def test_find_messages_by_id_from_data_provider(demo_data_source: HTTPProvider5DataSource):
    data_source = demo_data_source

    expected_message = {
        'attachedEventIds': [],
        'body': {'fields': {'header': {'messageValue': {'fields': {'BeginString': {'simpleValue': 'FIXT.1.1'},
                                                                   'BodyLength': {'simpleValue': '61'},
                                                                   'MsgSeqNum': {'simpleValue': '33'},
                                                                   'MsgType': {'simpleValue': '0'},
                                                                   'SenderCompID': {'simpleValue': 'ARFQ01FIX08'},
                                                                   'SendingTime': {
                                                                       'simpleValue': '2022-06-30T14:39:27.111'},
                                                                   'TargetCompID': {'simpleValue': 'FGW'}}}},
                            'trailer': {'messageValue': {'fields': {'CheckSum': {'simpleValue': '160'}}}}},
                 'metadata': {'id': {'connectionId': {'sessionAlias': 'arfq01fix08'},
                                     'direction': 'SECOND',
                                     'sequence': '1656599887515499033',
                                     'subsequence': [1]},
                              'messageType': 'Heartbeat',
                              'protocol': 'FIX',
                              'timestamp': '2022-06-30T14:39:27.112Z'}},
        'bodyBase64': 'OD1GSVhULjEuMQE5PTYxATM1PTABMzQ9MzMBNDk9QVJGUTAxRklYMDgBNTI9MjAyMjA2MzAtMTQ6Mzk6MjcuMTExMDAwATU2PUZHVwExMD0xNjAB',
        'direction': 'OUT',
        'messageId': 'arfq01fix08:second:1656599887515499033',
        'messageType': 'Heartbeat',
        'sessionId': 'arfq01fix08',
        'timestamp': {'epochSecond': 1656599967, 'nano': 112000000},
        'type': 'message'
    }

    expected_messages = []
    expected_messages.append(expected_message)
    expected_messages.append(
        {'attachedEventIds': [],
         'body': {'fields': {'DefaultApplVerID': {'simpleValue': '9'},
                             'EncryptMethod': {'simpleValue': '0'},
                             'HeartBtInt': {'simpleValue': '5'},
                             'Password': {'simpleValue': 'mit123'},
                             'ResetSeqNumFlag': {'simpleValue': 'true'},
                             'header': {'messageValue': {'fields': {'BeginString': {'simpleValue': 'FIXT.1.1'},
                                                                    'BodyLength': {'simpleValue': '91'},
                                                                    'MsgSeqNum': {'simpleValue': '1'},
                                                                    'MsgType': {'simpleValue': 'A'},
                                                                    'SenderCompID': {'simpleValue': 'ARFQ01DC03'},
                                                                    'SendingTime': {
                                                                        'simpleValue': '2022-06-30T14:46:03.911'},
                                                                    'TargetCompID': {'simpleValue': 'FGW'}}}},
                             'trailer': {'messageValue': {'fields': {'CheckSum': {'simpleValue': '161'}}}}},
                  'metadata': {'id': {'connectionId': {'sessionAlias': 'arfq01dc03'},
                                      'direction': 'SECOND',
                                      'sequence': '1656599850628059096',
                                      'subsequence': [1]},
                               'messageType': 'Logon',
                               'protocol': 'FIX',
                               'timestamp': '2022-06-30T14:46:03.915Z'}},
         'bodyBase64': 'OD1GSVhULjEuMQE5PTkxATM1PUEBMzQ9MQE0OT1BUkZRMDFEQzAzATUyPTIwMjIwNjMwLTE0OjQ2OjAzLjkxMQE1Nj1GR1cBOTg9MAExMDg9NQExNDE9WQE1NTQ9bWl0MTIzATExMzc9OQExMD0xNjEB',
         'direction': 'OUT',
         'messageId': 'arfq01dc03:second:1656599850628059096',
         'messageType': 'Logon',
         'sessionId': 'arfq01dc03',
         'timestamp': {'epochSecond': 1656600363, 'nano': 915000000},
         'type': 'message'}
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
        {'type': 'event', 'eventId': 'a2321a5b-f883-11ec-8225-52540095fac0', 'batchId': None, 'isBatched': False,
         'eventName': '[TS_1]5 partfill trades and cancel.', 'eventType': '',
         'endTimestamp': {'nano': 735114000, 'epochSecond': 1656600478},
         'startTimestamp': {'nano': 735039000, 'epochSecond': 1656600478}, 'parentEventId': None, 'successful': False,
         'attachedMessageIds': [], 'body': {}}
    ]
    case1 = [{'type': 'event', 'eventId': 'bb0da3a9-f883-11ec-aeb3-adf8526f5eec', 'batchId': None, 'isBatched': False,
              'eventName': "Received 'ExecutionReport' response message", 'eventType': 'message',
              'endTimestamp': {'nano': 428471000, 'epochSecond': 1656600520},
              'startTimestamp': {'nano': 428350000, 'epochSecond': 1656600520},
              'parentEventId': 'ba4e7257-f883-11ec-aeb3-adf8526f5eec', 'successful': True, 'attachedMessageIds': [],
              'body': [{'type': 'treeTable',
                        'rows': {'ExecID': {'type': 'row', 'columns': {'fieldValue': 'E0AmqxctTQGw'}},
                                 'OrderQty': {'type': 'row', 'columns': {'fieldValue': '20'}},
                                 'LastQty': {'type': 'row', 'columns': {'fieldValue': '20'}},
                                 'OrderID': {'type': 'row', 'columns': {'fieldValue': '00Amr2Sw36j1'}},
                                 'TransactTime': {'type': 'row',
                                                  'columns': {'fieldValue': '2022-06-30T14:48:39.526758'}},
                                 'GroupID': {'type': 'row', 'columns': {'fieldValue': '0'}},
                                 'trailer': {'type': 'collection',
                                             'rows': {'CheckSum': {'type': 'row', 'columns': {'fieldValue': '136'}}}},
                                 'Side': {'type': 'row', 'columns': {'fieldValue': '2'}},
                                 'OrdStatus': {'type': 'row', 'columns': {'fieldValue': '2'}},
                                 'TimeInForce': {'type': 'row', 'columns': {'fieldValue': '0'}},
                                 'SecurityID': {'type': 'row', 'columns': {'fieldValue': '5221001'}},
                                 'ExecType': {'type': 'row', 'columns': {'fieldValue': 'F'}},
                                 'TradeLiquidityIndicator': {'type': 'row', 'columns': {'fieldValue': 'R'}},
                                 'LastLiquidityInd': {'type': 'row', 'columns': {'fieldValue': '2'}},
                                 'LeavesQty': {'type': 'row', 'columns': {'fieldValue': '0'}},
                                 'CumQty': {'type': 'row', 'columns': {'fieldValue': '20'}},
                                 'LastPx': {'type': 'row', 'columns': {'fieldValue': '55'}},
                                 'TypeOfTrade': {'type': 'row', 'columns': {'fieldValue': '2'}},
                                 'TrdMatchID': {'type': 'row', 'columns': {'fieldValue': 'L2N1AYTNPW'}},
                                 'OrdType': {'type': 'row', 'columns': {'fieldValue': '2'}},
                                 'ClOrdID': {'type': 'row', 'columns': {'fieldValue': '1985282'}},
                                 'SecurityIDSource': {'type': 'row', 'columns': {'fieldValue': '8'}},
                                 'LastMkt': {'type': 'row', 'columns': {'fieldValue': 'XLOM'}},
                                 'OrderCapacity': {'type': 'row', 'columns': {'fieldValue': 'A'}},
                                 'SecondaryClOrdID': {'type': 'row', 'columns': {'fieldValue': '33333'}},
                                 'AccountType': {'type': 'row', 'columns': {'fieldValue': '1'}},
                                 'Price': {'type': 'row', 'columns': {'fieldValue': '55'}},
                                 'MDEntryID': {'type': 'row', 'columns': {'fieldValue': '00Amr2Sw36j1'}},
                                 'TradingParty': {'type': 'collection', 'rows': {'NoPartyIDs': {'type': 'collection',
                                                                                                'rows': {'0': {
                                                                                                    'type': 'collection',
                                                                                                    'rows': {
                                                                                                        'PartyRole': {
                                                                                                            'type': 'row',
                                                                                                            'columns': {
                                                                                                                'fieldValue': '76'}},
                                                                                                        'PartyID': {
                                                                                                            'type': 'row',
                                                                                                            'columns': {
                                                                                                                'fieldValue': 'ARFQ01FIX08'}},
                                                                                                        'PartyIDSource': {
                                                                                                            'type': 'row',
                                                                                                            'columns': {
                                                                                                                'fieldValue': 'D'}}}},
                                                                                                         '1': {
                                                                                                             'type': 'collection',
                                                                                                             'rows': {
                                                                                                                 'PartyRole': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '17'}},
                                                                                                                 'PartyID': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': 'ARFQ01'}},
                                                                                                                 'PartyIDSource': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': 'D'}}}},
                                                                                                         '2': {
                                                                                                             'type': 'collection',
                                                                                                             'rows': {
                                                                                                                 'PartyRole': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '3'}},
                                                                                                                 'PartyID': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '0'}},
                                                                                                                 'PartyIDSource': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': 'P'}}}},
                                                                                                         '3': {
                                                                                                             'type': 'collection',
                                                                                                             'rows': {
                                                                                                                 'PartyRole': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '122'}},
                                                                                                                 'PartyID': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '0'}},
                                                                                                                 'PartyIDSource': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': 'P'}}}},
                                                                                                         '4': {
                                                                                                             'type': 'collection',
                                                                                                             'rows': {
                                                                                                                 'PartyRole': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '12'}},
                                                                                                                 'PartyID': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': '3'}},
                                                                                                                 'PartyIDSource': {
                                                                                                                     'type': 'row',
                                                                                                                     'columns': {
                                                                                                                         'fieldValue': 'P'}}}}}}}},
                                 'header': {'type': 'collection', 'rows': {
                                     'BeginString': {'type': 'row', 'columns': {'fieldValue': 'FIXT.1.1'}},
                                     'SenderCompID': {'type': 'row', 'columns': {'fieldValue': 'FGW'}},
                                     'SendingTime': {'type': 'row',
                                                     'columns': {'fieldValue': '2022-06-30T14:48:39.530311'}},
                                     'TargetCompID': {'type': 'row', 'columns': {'fieldValue': 'ARFQ01FIX08'}},
                                     'ApplVerID': {'type': 'row', 'columns': {'fieldValue': '9'}},
                                     'MsgType': {'type': 'row', 'columns': {'fieldValue': '8'}},
                                     'MsgSeqNum': {'type': 'row', 'columns': {'fieldValue': '589'}},
                                     'BodyLength': {'type': 'row', 'columns': {'fieldValue': '432'}}}},
                                 'DisplayQty': {'type': 'row', 'columns': {'fieldValue': '0'}}}}]}]
    case3 = [
        {'type': 'message', 'timestamp': {'nano': 422000000, 'epochSecond': 1656600504},
         'messageType': 'NewOrderSingle', 'direction': 'OUT', 'sessionId': 'arfq01fix07', 'attachedEventIds': [],
         'messageId': 'arfq01fix07:second:1656599837520228626', 'body': {'metadata': {
            'id': {'connectionId': {'sessionAlias': 'arfq01fix07'}, 'direction': 'SECOND',
                   'sequence': '1656599837520228626', 'subsequence': [1]}, 'timestamp': '2022-06-30T14:48:24.422Z',
            'messageType': 'NewOrderSingle', 'protocol': 'FIX'}, 'fields': {'OrderQty': {'simpleValue': '200'},
                                                                            'OrdType': {'simpleValue': '2'},
                                                                            'ClOrdID': {'simpleValue': '1830410'},
                                                                            'SecurityIDSource': {'simpleValue': '8'},
                                                                            'OrderCapacity': {'simpleValue': 'A'},
                                                                            'TransactTime': {
                                                                                'simpleValue': '2022-06-30T14:47:59.032276'},
                                                                            'SecondaryClOrdID': {
                                                                                'simpleValue': '11111'},
                                                                            'AccountType': {'simpleValue': '1'},
                                                                            'trailer': {'messageValue': {'fields': {
                                                                                'CheckSum': {'simpleValue': '152'}}}},
                                                                            'Side': {'simpleValue': '1'},
                                                                            'Price': {'simpleValue': '55'},
                                                                            'TradingParty': {'messageValue': {
                                                                                'fields': {'NoPartyIDs': {'listValue': {
                                                                                    'values': [{'messageValue': {
                                                                                        'fields': {'PartyRole': {
                                                                                            'simpleValue': '76'},
                                                                                            'PartyID': {
                                                                                                'simpleValue': 'ARFQ01FIX07'},
                                                                                            'PartyIDSource': {
                                                                                                'simpleValue': 'D'}}}},
                                                                                        {'messageValue': {
                                                                                            'fields': {
                                                                                                'PartyRole': {
                                                                                                    'simpleValue': '3'},
                                                                                                'PartyID': {
                                                                                                    'simpleValue': '0'},
                                                                                                'PartyIDSource': {
                                                                                                    'simpleValue': 'P'}}}},
                                                                                        {'messageValue': {
                                                                                            'fields': {
                                                                                                'PartyRole': {
                                                                                                    'simpleValue': '122'},
                                                                                                'PartyID': {
                                                                                                    'simpleValue': '0'},
                                                                                                'PartyIDSource': {
                                                                                                    'simpleValue': 'P'}}}},
                                                                                        {'messageValue': {
                                                                                            'fields': {
                                                                                                'PartyRole': {
                                                                                                    'simpleValue': '12'},
                                                                                                'PartyID': {
                                                                                                    'simpleValue': '3'},
                                                                                                'PartyIDSource': {
                                                                                                    'simpleValue': 'P'}}}}]}}}}},
                                                                            'SecurityID': {'simpleValue': '5221001'},
                                                                            'header': {'messageValue': {'fields': {
                                                                                'BeginString': {
                                                                                    'simpleValue': 'FIXT.1.1'},
                                                                                'SenderCompID': {
                                                                                    'simpleValue': 'ARFQ01FIX07'},
                                                                                'SendingTime': {
                                                                                    'simpleValue': '2022-06-30T14:48:24.330'},
                                                                                'TargetCompID': {'simpleValue': 'FGW'},
                                                                                'MsgType': {'simpleValue': 'D'},
                                                                                'MsgSeqNum': {'simpleValue': '626'},
                                                                                'BodyLength': {'simpleValue': '263'}}}},
                                                                            'DisplayQty': {'simpleValue': '200'}}},
         'bodyBase64': 'OD1GSVhULjEuMQE5PTI2MwEzNT1EATM0PTYyNgE0OT1BUkZRMDFGSVgwNwE1Mj0yMDIyMDYzMC0xNDo0ODoyNC4zMzAwMDABNTY9RkdXATExPTE4MzA0MTABMjI9OAEzOD0yMDABNDA9MgE0ND01NQE0OD01MjIxMDAxATU0PTEBNjA9MjAyMjA2MzAtMTQ6NDc6NTkuMDMyMjc2ATUyNj0xMTExMQE1Mjg9QQE1ODE9MQExMTM4PTIwMAE0NTM9NAE0NDg9QVJGUTAxRklYMDcBNDQ3PUQBNDUyPTc2ATQ0OD0wATQ0Nz1QATQ1Mj0zATQ0OD0wATQ0Nz1QATQ1Mj0xMjIBNDQ4PTMBNDQ3PVABNDUyPTEyATEwPTE1MgE='}
    ]
    assert list(demo_get_messages_with_one_filter) == case3
    assert list(demo_get_messages_with_filters) == case3
    assert list(demo_get_events_with_one_filter) == case and len(case) is 1
    assert list(demo_get_events_with_filters) == case1 and len(case1) is 1


def test_find_message_by_id_from_data_provider_with_error(demo_data_source: HTTPProvider5DataSource):
    data_source = demo_data_source

    with pytest.raises(CommandError) as exc_info:
        data_source.command(http.GetMessageById("demo-conn_not_exist:first:1624005448022245399"))


def test_get_events_from_data_provider_with_error(demo_data_source: HTTPProvider5DataSource):
    data_source = demo_data_source

    events = data_source.command(http.GetEvents(start_timestamp="test", end_timestamp="test"))
    with pytest.raises(TypeError) as exc_info:
        list(events)
    assert "replace() takes no keyword arguments" in str(exc_info)


def test_get_messages_from_data_provider_with_error(demo_data_source: HTTPProvider5DataSource):
    data_source = demo_data_source

    events = data_source.command(http.GetMessages(start_timestamp="test", end_timestamp="test", stream="test"))
    with pytest.raises(TypeError) as exc_info:
        list(events)
    assert "replace() takes no keyword arguments" in str(exc_info)


def test_check_url_for_data_source():
    with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
        data_source = HTTPProvider5DataSource("http://test_test:8080/")
    assert "Max retries exceeded with url" in str(exc_info)


def test_messageIds_not_in_last_msg(demo_messages_from_data_source: Data):
    data = demo_messages_from_data_source
    data_lst = list(data)
    last_msg = data_lst[-1]
    assert "messageIds" not in last_msg


def test_get_messages_with_multiple_url(
        demo_messages_from_data_source_with_test_streams: Data,
        demo_messages_from_data_source: Data,
):
    messages = demo_messages_from_data_source_with_test_streams.use_cache(True)

    messages_hand_demo_expected = demo_messages_from_data_source
    messages_hand_demo_actual = messages.filter(lambda record: record.get("sessionId") == "arfq01fix07")

    assert (
            len(list(messages)) == 272
            and len(list(messages_hand_demo_actual)) == len(list(messages_hand_demo_expected)) == 239
    )


# def test_unprintable_character(demo_data_source: HTTPProvider5DataSource):
#     event = demo_data_source.command(http.GetEventById(("b85d9dca-6236-11ec-bc58-1b1c943c5c0d")))
#
#     assert "\x80" in event["body"][0]["value"] and event["body"][0]["value"] == "nobJjpBJkTuQMmscc4R\x80"


def test_attached_messages(demo_data_source: HTTPProvider5DataSource):
    events = demo_data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=0, second=0, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=15, minute=0, second=0, microsecond=0),
            attached_messages=True,
        )
    )

    assert events.filter(lambda event: event.get("attachedMessageIds")).len
