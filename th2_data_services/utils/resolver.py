from abc import ABC, abstractmethod


# # # EXPERIMENTAL
# def get__find_key(record: dict, key_to_find: str) -> str:
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
    def get_id(event):
        pass

    @staticmethod
    @abstractmethod
    def get_parent_id(event):
        pass

    @staticmethod
    @abstractmethod
    def get_status(event):
        pass

    @staticmethod
    @abstractmethod
    def get_name(event):
        pass

    @staticmethod
    @abstractmethod
    def get_batch_id(event):
        pass

    @staticmethod
    @abstractmethod
    def get_is_batched(event):
        pass

    @staticmethod
    @abstractmethod
    def get_type(event):
        pass

    @staticmethod
    @abstractmethod
    def get_start_timestamp(event):
        pass

    @staticmethod
    @abstractmethod
    def get_end_timestamp(event):
        pass

    @staticmethod
    @abstractmethod
    def get_attached_messages_ids(event):
        pass

    @staticmethod
    @abstractmethod
    def get_body(event):
        pass


class MessageFieldsResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_direction(message):
        pass

    @staticmethod
    @abstractmethod
    def get_session_id(message):
        pass

    @staticmethod
    @abstractmethod
    def get_type(message):
        pass

    @staticmethod
    @abstractmethod
    def get_connection_id(message):
        pass

    @staticmethod
    @abstractmethod
    def get_session_alias(message):
        pass

    @staticmethod
    @abstractmethod
    def get_subsequence(message):
        pass

    @staticmethod
    @abstractmethod
    def get_sequence(message):
        pass

    @staticmethod
    @abstractmethod
    def get_timestamp(message):
        pass

    @staticmethod
    @abstractmethod
    def get_body(message):
        pass

    @staticmethod
    @abstractmethod
    def get_body_base64(message):
        pass

    @staticmethod
    @abstractmethod
    def get_id(message):
        pass

    @staticmethod
    @abstractmethod
    def get_attached_event_ids(message):
        pass
