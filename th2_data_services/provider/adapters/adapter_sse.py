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
import warnings
from typing import Generator, Callable

from sseclient import Event as SSEEvent
from urllib3.exceptions import HTTPError
import orjson as json

from th2_data_services.interfaces import IAdapter
from th2_data_services.utils.json import BufferedJSONProcessor


class SSEAdapter(IAdapter):
    """SSE Adapter handles bytes from sse-stream into Dict object."""

    def __init__(self):
        warnings.warn("This class is deprecated please use StreamingSSEAdapter")

    def handle(self, record: SSEEvent) -> dict:
        """Adapter handler.

        Args:
            record: SSE Event.

        Returns:
            Dict object.
        """
        if record.event == "error":
            raise HTTPError(record.data)
        if record.event not in ["close", "keep_alive", "message_ids"]:
            try:
                return json.loads(record.data)
            except json.JSONDecodeError as e:
                raise ValueError(f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{record.data}")


class StreamingSSEAdapter(IAdapter):
    def __init__(self, json_processor: BufferedJSONProcessor):
        self.json_processor = json_processor
        self.events_types_blacklist = {"close", "keep_alive", "message_ids"}

    def handle(self, record: (Generator[SSEEvent, None, None], Callable)) -> Generator[dict, None, None]:
        if callable(record):
            stream = record()
        else:
            stream = record
        for event in stream:
            if event.event == "error":
                raise HTTPError(event.data)
            if event.event not in self.events_types_blacklist:
                yield from self.json_processor.decode(event.data)
        yield from self.json_processor.fin()


def get_default_sse_adapter():
    return StreamingSSEAdapter(BufferedJSONProcessor())
