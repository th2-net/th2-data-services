from dataclasses import dataclass

from th2_data_services.source_api import IEventStruct, IMessageStruct


@dataclass
class Provider5EventStruct(IEventStruct):
    """Interface for Event of data-provider v5."""

    EVENT_ID: str
    PARENT_EVENT_ID: str
    STATUS: str
    NAME: str
    TYPE: str
    BATCH_ID: str
    IS_BATCHED: str
    EVENT_TYPE: str
    END_TIMESTAMP: str
    START_TIMESTAMP: str
    ATTACHED_MESSAGED: str
    BODY: str


provider5_event_struct = Provider5EventStruct(
    EVENT_ID="eventId",
    PARENT_EVENT_ID="parentEventId",
    STATUS="successful",
    NAME="eventName",
    TYPE="type",
    BATCH_ID="batchId",
    IS_BATCHED="isBatched",
    EVENT_TYPE="eventType",
    END_TIMESTAMP="endTimestamp",
    START_TIMESTAMP="startTimestamp",
    ATTACHED_MESSAGED="attachedMessageIds",
    BODY="body",
)


@dataclass
class Provider5MessageStruct(IMessageStruct):
    """Interface for Message of data-provider v5."""

    DIRECTION: str
    SESSION_ID: str
    MESSAGE_TYPE: str
    TIMESTAMP: str
    BODY: str
    BODY_BASE64: str
    TYPE: str
    MESSAGE_ID: str
    ATTACHED_EVENT_IDS: str


provider5_message_struct = Provider5MessageStruct(
    DIRECTION="direction",
    SESSION_ID="sessionId",
    MESSAGE_TYPE="messageType",
    TIMESTAMP="timestamp",
    BODY="body",
    BODY_BASE64="bodyBase64",
    TYPE="type",
    MESSAGE_ID="messageId",
    ATTACHED_EVENT_IDS="attachedEventIds",
)
