from abc import ABC, abstractmethod


class IAdapter(ABC):
    @abstractmethod
    def handle(self, record):
        pass


class IMessageAdapter(IAdapter):
    @abstractmethod
    def handle(self, record: dict):
        pass


class IEventAdapter(IAdapter):
    pass
