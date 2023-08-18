#  Copyright 2023 Exactpro (Exactpro Systems Limited)
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

from th2_data_services.interfaces.utils.resolver import EventFieldResolver, MessageFieldResolver


class TH2Config:
    def __init__(self) -> None:
        """Global configuration for the DS library."""
        self.INTERACTIVE_MODE = False
        self.EVENT_FIELDS_RESOLVER: EventFieldResolver = None
        self.MESSAGE_FIELDS_RESOLVER: MessageFieldResolver = None
        self.MAX_PATH: int = 255  # OS limitation. Both Windows and Linux
        self.FORBIDDEN_CHARACTERS_IN_FILENAME: str = '<>:"|?*/\\'
        self.FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO: str = "_"

    def __str__(self):
        s = (
            f"INTERACTIVE_MODE={self.INTERACTIVE_MODE}\n"
            f"EVENT_FIELDS_RESOLVER={self.EVENT_FIELDS_RESOLVER}\n"
            f"MESSAGE_FIELDS_RESOLVER={self.MESSAGE_FIELDS_RESOLVER}"
            f"MAX_PATH={self.MAX_PATH}"
            f"FORBIDDEN_CHARACTERS_IN_FILENAME={self.FORBIDDEN_CHARACTERS_IN_FILENAME}"
            f"FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO={self.FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO}"
        )
        return s


options = TH2Config()
