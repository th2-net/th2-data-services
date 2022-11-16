all_message_bodies = [{
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
}, {
	'type': 'message',
	'timestamp': {
		'nano': 802350000,
		'epochSecond': 1668068118
	},
	'messageType': 'Incoming',
	'direction': 'IN',
	'sessionId': 'ds-lib-session2',
	'attachedEventIds': [],
	'messageId': 'ds-lib-session2:first:1668068118435545202',
	'body': {
		'metadata': {
			'id': {
				'connectionId': {
					'sessionAlias': 'ds-lib-session2'
				},
				'sequence': '1668068118435545202'
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
}, {
	'type': 'message',
	'timestamp': {
		'nano': 803361000,
		'epochSecond': 1668068118
	},
	'messageType': 'Outgoing',
	'direction': 'OUT',
	'sessionId': 'ds-lib-session1',
	'attachedEventIds': [],
	'messageId': 'ds-lib-session1:second:1668068118435545203',
	'body': {
		'metadata': {
			'id': {
				'connectionId': {
					'sessionAlias': 'ds-lib-session1'
				},
				'direction': 'SECOND',
				'sequence': '1668068118435545203'
			},
			'messageType': 'Outgoing',
			'protocol': 'json'
		},
		'fields': {
			'a': {
				'simpleValue': '123'
			}
		}
	},
	'bodyBase64': 'eyJhIjogIjEyMyJ9'
}, {
	'type': 'message',
	'timestamp': {
		'nano': 803361000,
		'epochSecond': 1668068118
	},
	'messageType': 'Outgoing',
	'direction': 'OUT',
	'sessionId': 'ds-lib-session2',
	'attachedEventIds': [],
	'messageId': 'ds-lib-session2:second:1668068118435545204',
	'body': {
		'metadata': {
			'id': {
				'connectionId': {
					'sessionAlias': 'ds-lib-session2'
				},
				'direction': 'SECOND',
				'sequence': '1668068118435545204'
			},
			'messageType': 'Outgoing',
			'protocol': 'json'
		},
		'fields': {
			'a': {
				'simpleValue': '123'
			}
		}
	},
	'bodyBase64': 'eyJhIjogIjEyMyJ9'
}]