from typing import List

from th2_data_services.adapter import change_pipeline_message


def test_adapter_with_id(messages_before_pipeline_adapter: List[dict], messages_after_pipeline_adapter: List[dict]):
    output = []
    for message in messages_before_pipeline_adapter:
        messages = change_pipeline_message(message)
        if isinstance(messages, dict):
            messages = [messages]
        output.extend(messages)

    assert len(output) == 11 and output == messages_after_pipeline_adapter


def test_find_sub_message_with_adapter(message_from_pipeline: dict):
    msg_id = message_from_pipeline.get("messageId") + ".5"
    message_from_pipeline = change_pipeline_message(message_from_pipeline)

    index = None
    if msg_id.find(".") != -1:
        msg_id, index = msg_id.split(".")[:-1], int(msg_id[-1])

    result = []
    if isinstance(message_from_pipeline, list):
        if index:
            for message in message_from_pipeline:
                if message["body"]["metadata"]["id"]["subsequence"][0] == index:
                    result.append(message)
                    break
        else:
            result += message_from_pipeline
    else:
        result.append(message_from_pipeline)

    assert result == [
        {
            "attachedEventIds": ["09960e51-1c6b-11ec-9d85-cd5454918fce", "09963563-1c6b-11ec-9d85-cd5454918fce"],
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
                    "id": {"connectionId": {"sessionAlias": "test-42"}, "sequence": "1632216515838617066", "subsequence": [5]},
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
        }
    ]


def test_find_messages_with_adapter(message_from_pipeline: dict):
    msg_id = message_from_pipeline.get("messageId")
    message_from_pipeline = change_pipeline_message(message_from_pipeline)

    index = None
    if msg_id.find(".") != -1:
        msg_id, index = msg_id.split(".")[:-1], int(msg_id[-1])

    result = []
    if isinstance(message_from_pipeline, list):
        if index:
            for message in message_from_pipeline:
                if message["body"]["metadata"]["id"]["subsequence"][0] == index:
                    result.append(message)
                    break
        else:
            result += message_from_pipeline
    else:
        result.append(message_from_pipeline)

    assert len(result) == 5
