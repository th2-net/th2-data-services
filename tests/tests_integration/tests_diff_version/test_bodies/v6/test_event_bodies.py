root_event_body = {
	'type': 'event',
	'eventId': 'a26078a4-6419-11ed-bfec-b48c9dc9ebfb',
	'batchId': None,
	'isBatched': False,
	'eventName': 'Set of auto-generated events for ds lib testing',
	'eventType': 'ds-lib-test-event',
	'endTimestamp': '2022-11-14T12:41:18.095247000Z',
	'startTimestamp': '2022-11-14T12:41:18.095247000Z',
	'parentEventId': None,
	'successful': True,
	'attachedMessageIds': [],
	'body': {}
}

plain_event_1_body = {
	'type': 'event',
	'eventId': 'a275f396-6419-11ed-a9e6-b48c9dc9ebfb',
	'batchId': None,
	'isBatched': False,
	'eventName': 'Plain event 1',
	'eventType': 'ds-lib-test-event',
	'endTimestamp': '2022-11-14T12:41:18.095247000Z',
	'startTimestamp': '2022-11-14T12:41:18.095247000Z',
	'parentEventId': 'a26078a4-6419-11ed-bfec-b48c9dc9ebfb',
	'successful': True,
	'attachedMessageIds': [],
	'body': 'ds-lib test body'
}

filter_event_3_body = {
	'type': 'event',
	'eventId': 'a2761aca-6419-11ed-aec1-b48c9dc9ebfb',
	'batchId': None,
	'isBatched': False,
	'eventName': 'Event for Filter test. FilterString-3',
	'eventType': 'ds-lib-test-event',
	'endTimestamp': '2022-11-14T12:41:18.096250000Z',
	'startTimestamp': '2022-11-14T12:41:18.096250000Z',
	'parentEventId': 'a26078a4-6419-11ed-bfec-b48c9dc9ebfb',
	'successful': True,
	'attachedMessageIds': [],
	'body': 'ds-lib test body. FilterString-3'
}