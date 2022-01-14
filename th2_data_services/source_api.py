from abc import ABC, abstractmethod


class ISourceAPI(ABC):
    """High level interface for Source API."""


# TODO - solve where to put it
class IEventStruct(ABC):
    """Just to mark Event Struct class.

    It should look like a class with constants.
    """


# TODO - solve where to put it
class IMessageStruct(ABC):
    """Just to mark Message Struct class.

    It should look like a class with constants.
    """


# TODO - solve where to put it
class IStub(ABC):
    @abstractmethod
    def build(self):
        pass


# TODO - solve where to put it
class IEventStub(IStub):
    """Just to mark Event Stub class."""


# TODO - solve where to put it
class IMessageStub(ABC):
    """Just to mark Message Stub class."""


# TODO - solve where to put it
class EventStub(IEventStub):
    def build(self, event_id, **kwargs):
        stub_template = {
            "attachedMessageIds": [],
            "batchId": "Broken_Event",
            "endTimestamp": {"nano": 0, "epochSecond": 0},
            "startTimestamp": {"nano": 0, "epochSecond": 0},
            "type": "event",
            "eventId": f"{event_id}",
            "eventName": "Broken_Event",
            "eventType": "Broken_Event",
            "parentEventId": "Broken_Event",
            "successful": None,
            "isBatched": None,
        }
