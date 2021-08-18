from pprint import pprint
from typing import List

from th2_data_services.data_source import DataSource


def test_find_events_by_id_from_data_provider(demo_data_source: DataSource):
    data_source = demo_data_source

    expected_event = {'attachedMessageIds': [],
                      'batchId': None,
                      'body': {},
                      'endTimestamp': {'epochSecond': 1624185888, 'nano': 169710000},
                      'eventId': '88a3ee80-d1b4-11eb-b0fb-199708acc7bc',
                      'eventName': 'Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for '
                                   'instrument INSTR1',
                      'eventType': '',
                      'isBatched': False,
                      'parentEventId': '84db48fc-d1b4-11eb-b0fb-199708acc7bc',
                      'startTimestamp': {'epochSecond': 1624185888, 'nano': 169672000},
                      'successful': True,
                      'type': 'event'}

    expected_events = []
    expected_events.append(expected_event)
    expected_events.append({'attachedMessageIds': ['demo-conn2:first:1624005448022245399',
                                                   'demo-log:first:1624029363623063053',
                                                   'demo-dc1:first:1624005475720919499',
                                                   'demo-conn1:second:1624005455622140289',
                                                   'demo-dc1:second:1624005475721015014',
                                                   'th2-hand-demo:first:1623852603564709030',
                                                   'demo-conn2:second:1624005448022426113',
                                                   'demo-dc2:second:1624005466840347015',
                                                   'demo-conn1:first:1624005455622011522',
                                                   'demo-dc2:first:1624005466840263372'],
                            'batchId': '6e3be13f-cab7-4653-8cb9-6e74fd95ade4',
                            'body': [{'data': "Checkpoint id '8c037f50-d1b4-11eb-ba78-1981398e00bd'",
                                      'type': 'message'}],
                            'endTimestamp': {'epochSecond': 1624185893, 'nano': 830158000},
                            'eventId': '6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e',
                            'eventName': 'Checkpoint',
                            'eventType': 'Checkpoint',
                            'isBatched': True,
                            'parentEventId': '8bc787fe-d1b4-11eb-bae5-57b0c4472880',
                            'startTimestamp': {'epochSecond': 1624185893, 'nano': 828017000},
                            'successful': True,
                            'type': 'event'})

    event = data_source.find_events_by_id_from_data_provider('88a3ee80-d1b4-11eb-b0fb-199708acc7bc')
    print(event)
    events = data_source.find_events_by_id_from_data_provider([
        '88a3ee80-d1b4-11eb-b0fb-199708acc7bc',
        '6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e',
    ])

    # Check types
    assert isinstance(event, dict)
    assert isinstance(events, list)

    # Check content.
    assert event == expected_event
    assert events == expected_events
    assert len(events) == 2


def test_find_messages_by_id_from_data_provider(demo_data_source: DataSource):
    data_source = demo_data_source

    expected_message = {'type': 'message',
                        'timestamp': {'nano': 123000000, 'epochSecond': 1624185872},
                        'direction': 'IN',
                        'sessionId': 'demo-conn2',
                        'messageType': 'Heartbeat',
                        'body': {'metadata': {'id': {'connectionId': {'sessionAlias': 'demo-conn2'},
                                                     'sequence': '1624005448022245399',
                                                     'subsequence': [1]},
                                              'timestamp': '2021-06-20T10:44:32.123Z',
                                              'messageType': 'Heartbeat'},
                                 'fields': {
                                     'trailer': {'messageValue': {'fields': {'CheckSum': {'simpleValue': '073'}}}},
                                     'header': {'messageValue': {'fields': {'BeginString': {'simpleValue': 'FIXT.1.1'},
                                                                            'SenderCompID': {'simpleValue': 'FGW'},
                                                                            'SendingTime': {
                                                                                'simpleValue': '2021-06-20T10:44:32.122'},
                                                                            'TargetCompID': {
                                                                                'simpleValue': 'DEMO-CONN2'},
                                                                            'MsgType': {'simpleValue': '0'},
                                                                            'MsgSeqNum': {'simpleValue': '1290'},
                                                                            'BodyLength': {'simpleValue': '59'}}}}}},
                        'bodyBase64': 'OD1GSVhULjEuMQE5PTU5ATM1PTABMzQ9MTI5MAE0OT1GR1cBNTI9MjAyMTA2MjAtMTA6NDQ6MzIuMTIyATU2PURFTU8tQ09OTjIBMTA9MDczAQ==',
                        'messageId': 'demo-conn2:first:1624005448022245399'}

    expected_messages = []
    expected_messages.append(expected_message)
    expected_messages.append({'type': 'message',
                              'timestamp': {'nano': 820976000, 'epochSecond': 1624029370},
                              'direction': 'IN',
                              'sessionId': 'demo-log',
                              'messageType': 'NewOrderSingle',
                              'body': {'metadata': {'id': {'connectionId': {'sessionAlias': 'demo-log'},
                                                           'sequence': '1624029363623063053',
                                                           'subsequence': [1]},
                                                    'timestamp': '2021-06-18T15:16:10.820976Z',
                                                    'messageType': 'NewOrderSingle'},
                                       'fields': {'OrderQty': {'simpleValue': '100'},
                                                  'OrdType': {'simpleValue': '2'},
                                                  'ClOrdID': {'simpleValue': '1687434'},
                                                  'SecurityIDSource': {'simpleValue': '8'},
                                                  'OrderCapacity': {'simpleValue': 'A'},
                                                  'TransactTime': {'simpleValue': '2020-11-24T13:58:26.270'},
                                                  'SecondaryClOrdID': {'simpleValue': '33333'},
                                                  'AccountType': {'simpleValue': '1'},
                                                  'trailer': {
                                                      'messageValue': {'fields': {'CheckSum': {'simpleValue': '209'}}}},
                                                  'Side': {'simpleValue': '2'},
                                                  'Price': {'simpleValue': '34'},
                                                  'TimeInForce': {'simpleValue': '3'},
                                                  'TradingParty': {
                                                      'messageValue': {'fields': {'NoPartyIDs': {'listValue': {
                                                          'values': [
                                                              {'messageValue': {
                                                                  'fields': {'PartyRole': {'simpleValue': '76'},
                                                                             'PartyID': {
                                                                                 'simpleValue': 'DEMO-CONN2'},
                                                                             'PartyIDSource': {
                                                                                 'simpleValue': 'D'}}}},
                                                              {'messageValue': {
                                                                  'fields': {'PartyRole': {'simpleValue': '3'},
                                                                             'PartyID': {'simpleValue': '0'},
                                                                             'PartyIDSource': {
                                                                                 'simpleValue': 'P'}}}},
                                                              {'messageValue': {
                                                                  'fields': {'PartyRole': {'simpleValue': '122'},
                                                                             'PartyID': {'simpleValue': '0'},
                                                                             'PartyIDSource': {
                                                                                 'simpleValue': 'P'}}}},
                                                              {'messageValue': {
                                                                  'fields': {'PartyRole': {'simpleValue': '12'},
                                                                             'PartyID': {'simpleValue': '3'},
                                                                             'PartyIDSource': {
                                                                                 'simpleValue': 'P'}}}}]}}}}},
                                                  'SecurityID': {'simpleValue': 'INSTR2'},
                                                  'header': {'messageValue': {
                                                      'fields': {'BeginString': {'simpleValue': 'FIXT.1.1'},
                                                                 'SenderCompID': {'simpleValue': 'DEMO-CONN2'},
                                                                 'SendingTime': {
                                                                     'simpleValue': '2020-11-24T10:58:26.317'},
                                                                 'TargetCompID': {'simpleValue': 'FGW'},
                                                                 'MsgType': {'simpleValue': 'D'},
                                                                 'MsgSeqNum': {'simpleValue': '443'},
                                                                 'BodyLength': {'simpleValue': '250'}}}}}},
                              'bodyBase64': 'OD1GSVhULjEuMQE5PTI1MAEzNT1EATM0PTQ0MwE0OT1ERU1PLUNPTk4yATUyPTIwMjAxMTI0LTEwOjU4OjI2LjMxNwE1Nj1GR1cBMTE9MTY4NzQzNAEyMj04ATM4PTEwMAE0MD0yATQ0PTM0ATQ4PUlOU1RSMgE1ND0yATU5PTMBNjA9MjAyMDExMjQtMTM6NTg6MjYuMjcwATUyNj0zMzMzMwE1Mjg9QQE1ODE9MQE0NTM9NAE0NDg9REVNTy1DT05OMgE0NDc9RAE0NTI9NzYBNDQ4PTABNDQ3PVABNDUyPTMBNDQ4PTABNDQ3PVABNDUyPTEyMgE0NDg9MwE0NDc9UAE0NTI9MTIBMTA9MjA5AQ==',
                              'messageId': 'demo-log:first:1624029363623063053'})

    message = data_source.find_messages_by_id_from_data_provider('demo-conn2:first:1624005448022245399')
    messages = data_source.find_messages_by_id_from_data_provider([
        'demo-conn2:first:1624005448022245399',
        'demo-log:first:1624029363623063053'
    ])

    # Check types
    assert isinstance(message, dict)
    assert isinstance(messages, list)

    # Check content.
    assert message == expected_message
    assert messages == expected_messages
    assert len(messages) == 2
