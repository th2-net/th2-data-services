from abc import ABC, abstractmethod


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

    @staticmethod
    @abstractmethod
    def get_fields(message):
        pass
