all_message_bodies_grpc = [{
	'messageId': 'ds-lib-session1:FIRST:1668429677955474101',
	'timestamp': {
		'epochSecond': 1668429677,
		'nano': 955474000
	},
	'bodyRaw': 'eyJhIjogIjEyMyJ9',
	'messageItem': [{
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session1'
					},
					'sequence': '1668429677955474101',
					'direction': 'FIRST',
					'subsequence': []
				},
				'messageType': 'Incoming',
				'properties': {
					'com.exactpro.th2.cradle.grpc.protocol': 'json'
				},
				'protocol': 'json'
			},
			'fields': {
				'a': {
					'simpleValue': '123'
				}
			}
		},
		'match': True
	}],
	'attachedEventId': []
}, {
	'messageId': 'ds-lib-session1:SECOND:1668429677955474103',
	'timestamp': {
		'epochSecond': 1668429678,
		'nano': 93249000
	},
	'bodyRaw': 'eyJhIjogIjEyMyJ9',
	'messageItem': [{
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session1'
					},
					'direction': 'SECOND',
					'sequence': '1668429677955474103',
					'subsequence': []
				},
				'messageType': 'Outgoing',
				'properties': {
					'com.exactpro.th2.cradle.grpc.protocol': 'json'
				},
				'protocol': 'json'
			},
			'fields': {
				'a': {
					'simpleValue': '123'
				}
			}
		},
		'match': True
	}],
	'attachedEventId': []
}, {
	'messageId': 'ds-lib-session2:FIRST:1668429677955474102',
	'timestamp': {
		'epochSecond': 1668429678,
		'nano': 93249000
	},
	'bodyRaw': 'eyJhIjogIjEyMyJ9',
	'messageItem': [{
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session2'
					},
					'sequence': '1668429677955474102',
					'direction': 'FIRST',
					'subsequence': []
				},
				'messageType': 'Incoming',
				'properties': {
					'com.exactpro.th2.cradle.grpc.protocol': 'json'
				},
				'protocol': 'json'
			},
			'fields': {
				'a': {
					'simpleValue': '123'
				}
			}
		},
		'match': True
	}],
	'attachedEventId': []
}, {
	'messageId': 'ds-lib-session1:FIRST:1668429677955474105',
	'timestamp': {
		'epochSecond': 1668429678,
		'nano': 94248000
	},
	'bodyRaw': 'eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMSJ9',
	'messageItem': [{
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session1'
					},
					'sequence': '1668429677955474105',
					'direction': 'FIRST',
					'subsequence': []
				},
				'messageType': 'Incoming',
				'properties': {
					'com.exactpro.th2.cradle.grpc.protocol': 'json'
				},
				'protocol': 'json'
			},
			'fields': {
				'msg_for_get_by_id_num': {
					'simpleValue': '1'
				}
			}
		},
		'match': True
	}],
	'attachedEventId': []
}, {
	'messageId': 'ds-lib-session2:SECOND:1668429677955474104',
	'timestamp': {
		'epochSecond': 1668429678,
		'nano': 94248000
	},
	'bodyRaw': 'eyJhIjogIjEyMyJ9',
	'messageItem': [{
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session2'
					},
					'direction': 'SECOND',
					'sequence': '1668429677955474104',
					'subsequence': []
				},
				'messageType': 'Outgoing',
				'properties': {
					'com.exactpro.th2.cradle.grpc.protocol': 'json'
				},
				'protocol': 'json'
			},
			'fields': {
				'a': {
					'simpleValue': '123'
				}
			}
		},
		'match': True
	}],
	'attachedEventId': []
}, {
	'messageId': 'ds-lib-session1:FIRST:1668429677955474106',
	'timestamp': {
		'epochSecond': 1668429678,
		'nano': 95247000
	},
	'bodyRaw': 'eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMiJ9',
	'messageItem': [{
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session1'
					},
					'sequence': '1668429677955474106',
					'direction': 'FIRST',
					'subsequence': []
				},
				'messageType': 'Incoming',
				'properties': {
					'com.exactpro.th2.cradle.grpc.protocol': 'json'
				},
				'protocol': 'json'
			},
			'fields': {
				'msg_for_get_by_id_num': {
					'simpleValue': '2'
				}
			}
		},
		'match': True
	}],
	'attachedEventId': []
}]