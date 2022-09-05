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
import json
from typing import Union

from th2_data_services.interfaces.adapter import IAdapter

from google.protobuf.json_format import MessageToDict
from th2_grpc_data_provider.data_provider_template_pb2 import EventData, MessageData


class GRPCObjectToDictAdapter(IAdapter):
    """GRPC Adapter decodes a GRPC object into a Dict object."""

    def handle(self, record: Union[MessageData, EventData]) -> dict:
        """Decodes MessageData or EventData as GRPC object into a Dict object.

        Args:
            record: MessageData/EventData.

        Returns:
            Dict object.
        """
        new_record = MessageToDict(record, including_default_value_fields=True)

        if isinstance(record, EventData):
            new_record["startTimestamp"] = {
                "epochSecond": record.start_timestamp.seconds,
                "nano": record.start_timestamp.nanos,
            }
            new_record["endTimestamp"] = {
                "epochSecond": record.end_timestamp.seconds,
                "nano": record.end_timestamp.nanos,
            }
        elif isinstance(record, MessageData):
            new_record["timestamp"] = {"epochSecond": record.timestamp.seconds, "nano": record.timestamp.nanos}

        try:
            new_record["body"] = json.loads(record.body)
        except (KeyError, AttributeError, json.JSONDecodeError):
            return new_record
        except Exception as e:
            raise Exception(f"{e}; Current record: {record}")
        return new_record
