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
from typing import Generator

from sseclient import Event as SSEEvent
from urllib3.exceptions import HTTPError

from th2_data_services.interfaces import IAdapter
from th2_data_services.utils.json import BufferedJSONProcessor


class SSEAdapter(IAdapter):
    """SSE Adapter handles bytes from sse-stream into Dict object."""

    def __init__(self):
        warnings.warn("This class is deprecated please use StreamingSSEAdapter")

    def handle(self, record: SSEEvent):
        return record


class StreamingSSEAdapter(IAdapter):
    def __init__(self, json_processor: BufferedJSONProcessor):
        self.json_processor = json_processor
        self.events_types_blacklist = {"close", "keep_alive", "message_ids"}

    def handle(self, record: Generator[SSEEvent, None, None]) -> Generator[dict, None, None]:
        for event in record:
            if event.event == "error":
                raise HTTPError(event.data)
            if event.event not in self.events_types_blacklist:
                yield from self.json_processor.decode(event.data)


def get_default_sse_adapter():
    return StreamingSSEAdapter(BufferedJSONProcessor())
