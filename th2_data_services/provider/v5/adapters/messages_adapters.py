from th2_data_services.adapter import IMessageAdapter
from th2_data_services.provider.v5.struct import Provider5MessageStruct, provider5_message_struct


class AdapterDeleteMessageWrappers(IMessageAdapter):
    """Adapter that delete unnecessary wrappers in events.

    It use for message to which an AdaptorGRPCObjectToDict has been applied.
    """

    def __init__(self, message_struct: Provider5MessageStruct = provider5_message_struct):
        """
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
