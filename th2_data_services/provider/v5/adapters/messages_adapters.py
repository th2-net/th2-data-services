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

from th2_data_services.interfaces.adapter import IMessageAdapter
from th2_data_services.provider.v5.struct import Provider5MessageStruct, provider5_message_struct


class AdapterDeleteMessageWrappers(IMessageAdapter):
    """Adapter that delete unnecessary wrappers in events.

    It used for message to which an AdaptorGRPCObjectToDict has been applied.
    """

    def __init__(self, message_struct: Provider5MessageStruct = provider5_message_struct):
        """AdapterDeleteMessageWrappers constructor.

        Args:
            message_struct: Message struct.
        """
        self._message_struct = message_struct

    def handle(self, message: dict) -> dict:
        """Deletes unnecessary wrappers for field message_id.

        Args:
            message: Message.

        Returns:
            Message without wrappers.
        """
        message_id_field = self._message_struct.MESSAGE_ID

        message_id = message.get(message_id_field)

        session = message_id.get(self._message_struct.CONNECTION_ID, {}).get(self._message_struct.SESSION_ALIAS)
        direction = message_id.get(self._message_struct.DIRECTION)
        sequence = message_id.get(self._message_struct.SEQUENCE)

        message_id = f"{session}:{direction}:{sequence}"
        message[message_id_field] = message_id

        return message
