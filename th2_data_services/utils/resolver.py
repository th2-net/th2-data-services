from th2_data_services import EVENT_STRUCT, MESSAGE_STRUCT


# def _find_key(record: dict, key_to_find: str) -> str:
#     if key_to_find in record:
#         return key_to_find
#
#     key_to_find = key_to_find.lower()
#     for key in record:
#         if key_to_find == key.lower():
#             return key
#
#
# class FieldResolver:
#
#     @staticmethod
#     def get(record, key):
#         key = _find_key(record, key)
#         if not key:
#             raise KeyError(key)
#         return record[key]

# @staticmethod
# def find(record, key):
#     key = _find_key(record, key)
#     return record.get(key)


class GetEventFields:
    @staticmethod
    def id(self, event):
        return event[EVENT_STRUCT.EVENT_ID]

    @staticmethod
    def parent_id(self, event):
        return event[EVENT_STRUCT.PARENT_EVENT_ID]

    @staticmethod
    def status(self, event):
        return event[EVENT_STRUCT.STATUS]

    @staticmethod
    def name(self, event):
        return event[EVENT_STRUCT.NAME]

    @staticmethod
    def batch_id(self, event):
        return event[EVENT_STRUCT.BATCH_ID]

    @staticmethod
    def is_batched(self, event):
        return event[EVENT_STRUCT.IS_BATCHED]

    @staticmethod
    def type(self, event):
        return event[EVENT_STRUCT.EVENT_TYPE]

    @staticmethod
    def start_timestamp(self, event):
        return event[EVENT_STRUCT.START_TIMESTAMP]

    @staticmethod
    def end_timestamp(self, event):
        return event[EVENT_STRUCT.END_TIMESTAMP]

    @staticmethod
    def attached_messages_ids(self, event):
        return event[EVENT_STRUCT.ATTACHED_MESSAGES_IDS]

    @staticmethod
    def body(self, event):
        return event[EVENT_STRUCT.BODY]


class GetMessageFields:
    @staticmethod
    def direction(self, message):
        return message[MESSAGE_STRUCT.DIRECTION]

    @staticmethod
    def session_id(self, message):
        return message[MESSAGE_STRUCT.SESSION_ID]

    @staticmethod
    def type(self, message):
        return message[MESSAGE_STRUCT.MESSAGE_TYPE]

    @staticmethod
    def connection_id(self, message):
        return message[MESSAGE_STRUCT.CONNECTION_ID]

    @staticmethod
    def session_alias(self, message):
        return message[MESSAGE_STRUCT.SESSION_ALIAS]

    @staticmethod
    def subsequence(self, message):
        return message[MESSAGE_STRUCT.SUBSEQUENCE]

    @staticmethod
    def sequence(self, message):
        return message[MESSAGE_STRUCT.SEQUENCE]

    @staticmethod
    def timestamp(self, message):
        return message[MESSAGE_STRUCT.TIMESTAMP]

    @staticmethod
    def body(self, message):
        return message[MESSAGE_STRUCT.BODY]

    @staticmethod
    def body_base64(self, message):
        return message[MESSAGE_STRUCT.BODY_BASE64]

    @staticmethod
    def id(self, message):
        return message[MESSAGE_STRUCT.MESSAGE_ID]

    @staticmethod
    def attached_event_ids(self, message):
        return message[MESSAGE_STRUCT.ATTACHED_EVENT_IDS]
