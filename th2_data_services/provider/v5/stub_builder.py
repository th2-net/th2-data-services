from th2_data_services.provider.stub_builder import IEventStub, IMessageStub
from th2_data_services.provider.v5.struct import provider5_event_struct, provider5_message_struct


class Provider5EventStubBuilder(IEventStub):
    def __init__(self, event_struct=provider5_event_struct):
        super().__init__()
        self.event_fields = event_struct

    @property
    def template(self) -> dict:
        return {
            self.event_fields.ATTACHED_MESSAGES_IDS: [],
            self.event_fields.BATCH_ID: "Broken_Event",
            self.event_fields.END_TIMESTAMP: {"nano": 0, "epochSecond": 0},
            self.event_fields.START_TIMESTAMP: {"nano": 0, "epochSecond": 0},
            self.event_fields.TYPE: "event",
            self.event_fields.EVENT_ID: self.REQUIRED_FIELD,
            self.event_fields.NAME: "Broken_Event",
            self.event_fields.EVENT_TYPE: "Broken_Event",
            self.event_fields.PARENT_EVENT_ID: "Broken_Event",
            self.event_fields.STATUS: None,
            self.event_fields.IS_BATCHED: None,
        }


class Provider5MessageStubBuilder(IMessageStub):
    def __init__(self, message_struct=provider5_message_struct):
        super().__init__()
        self.message_fields = message_struct

    @property
    def template(self) -> dict:
        # TODO - will be implemented by Grigory
        pass


provider5_event_stub_builder = Provider5EventStubBuilder()
provider5_message_stub_builder = Provider5EventStubBuilder()
