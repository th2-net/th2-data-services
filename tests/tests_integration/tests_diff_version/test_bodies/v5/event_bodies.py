root_event_body = {
    "type": "event",
    "eventId": "9daac0e5-65ad-11ed-a742-b48c9dc9ebfb",
    "batchId": None,
    "isBatched": False,
    "eventName": "Set of auto-generated events for ds lib testing",
    "eventType": "ds-lib-test-event",
    "endTimestamp": {"nano": 307080000, "epochSecond": 1668603187},
    "startTimestamp": {"nano": 307080000, "epochSecond": 1668603187},
    "parentEventId": None,
    "successful": True,
    "attachedMessageIds": [],
    "body": {},
}

plain_event_1_body = {
    "type": "event",
    "eventId": "9e02c395-65ad-11ed-83f9-b48c9dc9ebfb",
    "batchId": None,
    "isBatched": False,
    "eventName": "Plain event 1",
    "eventType": "ds-lib-test-event",
    "endTimestamp": {"nano": 308226000, "epochSecond": 1668603187},
    "startTimestamp": {"nano": 308226000, "epochSecond": 1668603187},
    "parentEventId": "9daac0e5-65ad-11ed-a742-b48c9dc9ebfb",
    "successful": True,
    "attachedMessageIds": [],
    "body": "ds-lib test body",
}

filter_event_3_body = {
    "type": "event",
    "eventId": "9e02c3a1-65ad-11ed-9475-b48c9dc9ebfb",
    "batchId": None,
    "isBatched": False,
    "eventName": "Event for Filter test. FilterString-3",
    "eventType": "ds-lib-test-event",
    "endTimestamp": {"nano": 308226000, "epochSecond": 1668603187},
    "startTimestamp": {"nano": 308226000, "epochSecond": 1668603187},
    "parentEventId": "9daac0e5-65ad-11ed-a742-b48c9dc9ebfb",
    "successful": True,
    "attachedMessageIds": [],
    "body": "ds-lib test body. FilterString-3",
}
