from abc import ABC
from dataclasses import dataclass


@dataclass
class IProviderEvent(ABC):
    """The interface that all classes of the library refer to.

    If this interface will be changed it invokes changes in the lib classes.
    The major version will be increased.
    """

    EVENT_ID: str
    PARENT_EVENT_ID: str
    STATUS: str
    NAME: str


ICurrentProviderEvent = IProviderEvent
