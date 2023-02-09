from abc import ABC, abstractmethod


# # # EXPERIMENTAL
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
#
#     @staticmethod
#     def find(record, key):
#         key = _find_key(record, key)
#         return record.get(key)
# # # EXPERIMENTAL


class EventFieldsResolver(ABC):
    @staticmethod
    @abstractmethod
    def id(self, event):
        pass

    @staticmethod
    @abstractmethod
    def parent_id(self, event):
        pass

    @staticmethod
    @abstractmethod
    def status(self, event):
        pass

    @staticmethod
    @abstractmethod
    def name(self, event):
        pass

    @staticmethod
    @abstractmethod
    def batch_id(self, event):
        pass

    @staticmethod
    @abstractmethod
    def is_batched(self, event):
        pass

    @staticmethod
    @abstractmethod
    def type(self, event):
        pass

    @staticmethod
    @abstractmethod
    def start_timestamp(self, event):
        pass

    @staticmethod
    @abstractmethod
    def end_timestamp(self, event):
        pass

    @staticmethod
    @abstractmethod
    def attached_messages_ids(self, event):
        pass

    @staticmethod
    @abstractmethod
    def body(self, event):
        pass


class MessageFieldsResolver(ABC):
    @staticmethod
    @abstractmethod
    def direction(self, message):
        pass

    @staticmethod
    @abstractmethod
    def session_id(self, message):
        pass

    @staticmethod
    @abstractmethod
    def type(self, message):
        pass

    @staticmethod
    @abstractmethod
    def connection_id(self, message):
        pass

    @staticmethod
    @abstractmethod
    def session_alias(self, message):
        pass

    @staticmethod
    @abstractmethod
    def subsequence(self, message):
        pass

    @staticmethod
    @abstractmethod
    def sequence(self, message):
        pass

    @staticmethod
    @abstractmethod
    def timestamp(self, message):
        pass

    @staticmethod
    @abstractmethod
    def body(self, message):
        pass

    @staticmethod
    @abstractmethod
    def body_base64(self, message):
        pass

    @staticmethod
    @abstractmethod
    def id(self, message):
        pass

    @staticmethod
    @abstractmethod
    def attached_event_ids(self, message):
        pass
