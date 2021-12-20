from dataclasses import dataclass
from th2_data_services.provider_api.event import IProviderEvent


@dataclass
class Provider5Event(IProviderEvent):
    """Interface for Event of data-provider v5."""

    TYPE: str
    BATCH_ID: str
    IS_BATCHED: str
    EVENT_TYPE: str
    END_TIMESTAMP: str
    START_TIMESTAMP: str
    ATTACHED_MESSAGED: str
    BODY: str


provider5_http_event = Provider5Event(
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
