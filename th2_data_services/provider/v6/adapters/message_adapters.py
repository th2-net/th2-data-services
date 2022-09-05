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
import pprint
from _warnings import warn
from typing import Union, List

from th2_data_services.interfaces.adapter import IMessageAdapter
from th2_data_services.provider.v6.struct import HTTPProvider6MessageStruct, grpc_provider6_message_struct


class DeleteMessageWrappersAdapter(IMessageAdapter):
    """Adapter that deletes unnecessary wrappers in messages.

    It used for the message to which an AdaptorGRPCObjectToDict has been applied.
    """

    def __init__(self, message_struct: HTTPProvider6MessageStruct = grpc_provider6_message_struct):
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

        message_id = message[message_id_field]

        session = message_id[self._message_struct.CONNECTION_ID][self._message_struct.SESSION_ALIAS]
        direction = message_id[self._message_struct.DIRECTION]
        sequence = message_id[self._message_struct.SEQUENCE]

        message_id = f"{session}:{direction}:{sequence}"
        message[message_id_field] = message_id

        return message


class CodecPipelinesAdapter(IMessageAdapter):
    """Adapter for codec-pipeline messages from provider v6.

    Codec-pipeline messages have sub-messages in the body.
    This adapter used for split codec-pipeline message to separate messages.
    """

    def __init__(self, ignore_errors=False):
        """AdapterCodecPipelines constructor.

        Args:
            ignore_errors: If True it will ignore errors and return message as is.
        """
        self._ignore_errors = ignore_errors

    def handle(self, message: dict) -> Union[List[dict], dict]:
        """Adapter handler.

        Args:
            message: Th2Message dict.

        Returns:
            Th2Message dict.
        """
        msg_type = message.get("messageType")
        if msg_type is None:
            if self._ignore_errors:
                warn(
                    "Please note, some messages don't have a messageType field. Perhaps a codec didn't decode them.",
                    stacklevel=3,
                )
                return message
            else:
                raise ValueError(
                    "The messages doesn't have a messageType field. Message:\n" f"{pprint.pformat(message)}"
                )

        if "/" not in msg_type:
            return message

        body = message["body"]
        if not body:
            return message

        sub_messages = []
        fields = body["fields"]
        if not fields:
            return message

        for sub_msg in fields:
            split_msg_name = sub_msg.split("-")
            if len(split_msg_name) > 1:
                sub_msg_type, index = "".join(split_msg_name[:-1]), int(split_msg_name[-1])
            else:
                index = msg_type.split("/").index(sub_msg) + 1
                sub_msg_type = sub_msg

            new_record = message.copy()

            metadata = new_record["body"]["metadata"].copy()
            id_field = metadata["id"].copy()
            id_field["subsequence"] = [index]
            metadata["id"] = id_field

            body_fields = fields[sub_msg]
            metadata.update(body_fields.get("metadata", {}))

            body = {"metadata": metadata}
            if body_fields.get("messageValue"):
                body = {**body_fields["messageValue"], **body}
            elif body_fields.get("fields"):
                body = {**body_fields["fields"], **body}
            else:
                body = {"fields": {}, **body}

            new_record["body"] = body
            new_record["body"]["metadata"]["messageType"] = sub_msg_type
            new_record["messageType"] = sub_msg_type
            new_record["messageId"] = f"{message['messageId']}.{index}"
            sub_messages.append(new_record)

        return sub_messages
