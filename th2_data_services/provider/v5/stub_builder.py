#  Copyright 2022 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from th2_data_services.provider.interfaces.stub_builder import IEventStub, IMessageStub
from th2_data_services.provider.v5.struct import (
    provider5_event_struct,
    provider5_message_struct,
)


class Provider5EventStubBuilder(IEventStub):
    def __init__(self, event_struct=provider5_event_struct):
        """Event stub builder for Provider v5.

        Args:
            event_struct: Event struct class.
        """
        self.event_fields = event_struct
        super().__init__()  # Requirement to define fields for the template earlier.

    @property
    def template(self) -> dict:
        """Event stub template.

        Returns:
            (dict) Event stub template.
        """
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
        """Event stub builder for Provider v5.

        Args:
            message_struct: Message struct class.
        """
        self.message_fields = message_struct
        super().__init__()  # Requirement to define fields for the template earlier.

    @property
    def template(self) -> dict:
        """Message stub template.

        Returns:
            (dict) Message stub template.
        """
        return {
            self.message_fields.DIRECTION: None,
            self.message_fields.SESSION_ID: "Broken_Message",
            self.message_fields.MESSAGE_TYPE: "Broken_Message",
            self.message_fields.TIMESTAMP: {"nano": 0, "epochSecond": 0},
            self.message_fields.BODY: [],
            self.message_fields.BODY_BASE64: [],
            self.message_fields.TYPE: "message",
            self.message_fields.MESSAGE_ID: self.REQUIRED_FIELD,
            self.message_fields.ATTACHED_EVENT_IDS: [],
        }


provider5_event_stub_builder = Provider5EventStubBuilder()
provider5_message_stub_builder = Provider5MessageStubBuilder()
