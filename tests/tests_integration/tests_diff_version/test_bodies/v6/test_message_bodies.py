message_1_body = {
	'type': 'message',
	'id': 'ds-lib-session1:first:1668429677955474106',
	'timestamp': '2022-11-14T12:41:18.095247000Z',
	'sessionId': 'ds-lib-session1',
	'direction': 'FIRST',
	'sequence': '1668429677955474106',
	'attachedEventIds': [],
	'rawMessageBase64': 'eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMiJ9',
	'parsedMessages': [{
		'match': True,
		'id': 'ds-lib-session1:first:1668429677955474106.',
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session1'
					},
					'sequence': '1668429677955474106'
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
		}
	}]
}

message_2_body = {
	'type': 'message',
	'id': 'ds-lib-session1:first:1668429677955474105',
	'timestamp': '2022-11-14T12:41:18.094248000Z',
	'sessionId': 'ds-lib-session1',
	'direction': 'FIRST',
	'sequence': '1668429677955474105',
	'attachedEventIds': [],
	'rawMessageBase64': 'eyJtc2dfZm9yX2dldF9ieV9pZF9udW0iOiAiMSJ9',
	'parsedMessages': [{
		'match': True,
		'id': 'ds-lib-session1:first:1668429677955474105.',
		'message': {
			'metadata': {
				'id': {
					'connectionId': {
						'sessionAlias': 'ds-lib-session1'
					},
					'sequence': '1668429677955474105'
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
		}
	}]
}