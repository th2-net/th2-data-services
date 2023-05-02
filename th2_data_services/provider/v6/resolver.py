from th2_data_services.interfaces.utils.resolver import EventFieldsResolver, MessageFieldsResolver
from th2_data_services.provider.v6.struct import http_provider6_event_struct, http_provider6_message_struct

class Provider6EventFieldsResolver(EventFieldsResolver):
    @staticmethod
    def get_id(event):
        return event[http_provider6_event_struct.EVENT_ID]

    @staticmethod
    def get_parent_id(event):
        return event[http_provider6_event_struct.PARENT_EVENT_ID]

    @staticmethod
    def get_status(event):
        return event[http_provider6_event_struct.STATUS]

    @staticmethod
    def get_name(event):
        return event[http_provider6_event_struct.NAME]

    @staticmethod
    def get_batch_id(event):
        return event[http_provider6_event_struct.BATCH_ID]

    @staticmethod
    def get_is_batched(event):
        return event[http_provider6_event_struct.IS_BATCHED]

    @staticmethod
    def get_type(event):
        return event[http_provider6_event_struct.EVENT_TYPE]

    @staticmethod
    def get_start_timestamp(event):
        return event[http_provider6_event_struct.START_TIMESTAMP]

    @staticmethod
    def get_end_timestamp(event):
        return event[http_provider6_event_struct.END_TIMESTAMP]

    @staticmethod
    def get_attached_messages_ids(event):
        return event[http_provider6_event_struct.ATTACHED_MESSAGES_IDS]

    @staticmethod
    def get_body(event):
        return event[http_provider6_event_struct.BODY]


class Provider6MessageFieldsResolver(MessageFieldsResolver):
    @staticmethod
    def get_subsequence(message):
        raise NotImplementedError

    @staticmethod
    def get_direction(message):
        return message[http_provider6_message_struct.DIRECTION]

    @staticmethod
    def get_session_id(message):
        return message[http_provider6_message_struct.SESSION_ID]

    @staticmethod
    def get_type(message):
        if len(message[http_provider6_message_struct.BODY]) == 1:
            return message[http_provider6_message_struct.BODY][0]["message"]["metadata"][http_provider6_message_struct.MESSAGE_TYPE]
        else:
            raise(Exception("More than one item in parsedMessages"))
    @staticmethod
    def get_connection_id(message):
        if len(message[http_provider6_message_struct.BODY]) == 1:
            return message[http_provider6_message_struct.BODY][0]["message"]["metadata"]["id"][http_provider6_message_struct.CONNECTION_ID]
        else:
            raise(Exception("More than one item in parsedMessages"))

    @staticmethod
    def get_session_alias(message):
        if len(message[http_provider6_message_struct.BODY]) == 1:
            return message[http_provider6_message_struct.BODY][0]["message"]["metadata"]["id"][http_provider6_message_struct.CONNECTION_ID][http_provider6_message_struct.SESSION_ALIAS]
        else:
            raise(Exception("More than one item in parsedMessages"))

    @staticmethod
    def get_sequence(message):
        return message[http_provider6_message_struct.SEQUENCE]

    @staticmethod
    def get_timestamp(message):
        return message[http_provider6_message_struct.TIMESTAMP]

    @staticmethod
    def get_body(message):
        return message[http_provider6_message_struct.BODY]

    @staticmethod
    def get_body_base64(message):
        return message[http_provider6_message_struct.BODY_BASE64]

    @staticmethod
    def get_id(message):
        return message[http_provider6_message_struct.MESSAGE_ID]

    @staticmethod
    def get_attached_event_ids(message):
        return message[http_provider6_message_struct.ATTACHED_EVENT_IDS]

    @staticmethod
    # message body in rdp6 is a list. we should which field or maybe list of fields to return
    def get_fields(message):
        if len(message[http_provider6_message_struct.BODY]) == 1:
            return message[http_provider6_message_struct.BODY][0]["message"]["fields"]
        else:
            raise(Exception("More than one item in parsedMessages"))