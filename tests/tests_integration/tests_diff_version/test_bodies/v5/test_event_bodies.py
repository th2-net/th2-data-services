root_event_body = {
	'type': 'message',
	'timestamp': {
		'nano': 435545000,
		'epochSecond': 1668068118
	},
	'messageType': 'Incoming',
	'direction': 'IN',
	'sessionId': 'ds-lib-session1',
	'attachedEventIds': [],
	'messageId': 'ds-lib-session1:first:1668068118435545201',
	'body': {
		'metadata': {
			'id': {
				'connectionId': {
					'sessionAlias': 'ds-lib-session1'
				},
				'sequence': '1668068118435545201'
			},
			'messageType': 'Incoming',
			'protocol': 'json'
		},
		'fields': {
			'a': {
				'simpleValue': '123'
			}
		}
	},
	'bodyBase64': 'eyJhIjogIjEyMyJ9'
}

plain_event_1_body = {
	'eventId': '24aae778-6017-11ed-b87c-b48c9dc9ebfa',
	'parentEventId': '2479e531-6017-11ed-9d54-b48c9dc9ebfa',
	'startTimestamp': {
		'epochSecond': 1667988803,
		'nano': 404786000
	},
	'endTimestamp': {
		'epochSecond': 1667988803,
		'nano': 404786000
	},
	'eventName': 'Plain event 1',
	'eventType': 'ds-lib-test-event',
	'body': 'ds-lib test body',
	'isBatched': False,
	'successful': 'SUCCESS',
	'attachedMessageIds': []
}

filter_event_3_body = {
	'eventId': '24ab19ed-6017-11ed-98bf-b48c9dc9ebfa',
	'parentEventId': '2479e531-6017-11ed-9d54-b48c9dc9ebfa',
	'startTimestamp': {
		'epochSecond': 1667988803,
		'nano': 406077000
	},
	'endTimestamp': {
		'epochSecond': 1667988803,
		'nano': 406077000
	},
	'eventName': 'Event for Filter test. FilterString-3',
	'eventType': 'ds-lib-test-event',
	'body': 'ds-lib test body. FilterString-3',
	'isBatched': False,
	'successful': 'SUCCESS',
	'attachedMessageIds': []
}