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

from sseclient import Event as SSEEvent
from urllib3.exceptions import HTTPError
import json

from th2_data_services.interfaces import IAdapter


class SSEAdapter(IAdapter):
    """SSE Adapter handles bytes from sse-stream into Dict object."""

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
