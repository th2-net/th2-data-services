import json
from typing import Union
from sseclient import Event as SSEEvent
from urllib3.exceptions import HTTPError

from th2_data_services.adapter import IAdapter

from google.protobuf.json_format import MessageToDict
from th2_grpc_data_provider.data_provider_template_pb2 import EventData, MessageData


class AdapterGRPCObjectToDict(IAdapter):
    """GRPC Adapter decodes a GRPC object into a Dict object."""

    def handle(self, record: Union[MessageData, EventData]) -> dict:
        """Decodes MessageData or EventData as GRPC object into a Dict object.

        Args:
            record: MessageData/EventData.

        Returns:
            Dict object.
        """
        new_record = MessageToDict(record, including_default_value_fields=True)
        try:
            new_record["body"] = json.loads(record.body)
        except (KeyError, json.JSONDecodeError):
            return new_record
        return new_record


class AdapterSSE(IAdapter):
    """SSE Adapter handle bytes from sse-stream into Dict object."""

    def handle(self, record: SSEEvent) -> dict:
        """SSE adapter.

        Args:
            record: SSE Event

        Returns:
            Dict object.
        """
        if record.event == "error":
            raise HTTPError(record.data)
        if record.event not in ["close", "keep_alive", "message_ids"]:
            try:
                return json.loads(record.data)
            except json.JSONDecodeError as e:
                raise Exception(f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{record.data}")
