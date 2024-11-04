#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
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
from typing import Optional

from th2_data_services.interfaces.utils.resolver import (
    EventFieldResolver,
    MessageFieldResolver,
    SubMessageFieldResolver,
    ExpandedMessageFieldResolver,
)


class TH2Config:
    def __init__(self) -> None:
        """Global configuration for the DS library."""
        # TODO - try to import here data_source in available.

        self.INTERACTIVE_MODE = False
        self.EVENT_FIELDS_RESOLVER: Optional[EventFieldResolver] = None
        self.MESSAGE_FIELDS_RESOLVER: Optional[MessageFieldResolver] = None
        self.SUBMESSAGE_FIELDS_RESOLVER: Optional[SubMessageFieldResolver] = None
        self.EXPANDED_MESSAGE_FIELDS_RESOLVER: Optional[ExpandedMessageFieldResolver] = None
        self.MAX_PATH: int = 255  # OS limitation. Both Windows and Linux
        self.FORBIDDEN_CHARACTERS_IN_FILENAME: str = '<>:"|?*/\\'
        self.FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO: str = "_"
        self.DEFAULT_PICKLE_VERSION = 4

        # Aliases
        self.efr = self.EVENT_FIELDS_RESOLVER
        self.mfr = self.MESSAGE_FIELDS_RESOLVER
        self.smfr = self.SUBMESSAGE_FIELDS_RESOLVER
        self.emfr = self.EXPANDED_MESSAGE_FIELDS_RESOLVER

    def __str__(self):
        s = (
            f"INTERACTIVE_MODE={self.INTERACTIVE_MODE}\n"
            f"EVENT_FIELDS_RESOLVER={self.EVENT_FIELDS_RESOLVER}\n"
            f"MESSAGE_FIELDS_RESOLVER={self.MESSAGE_FIELDS_RESOLVER}\n"
            f"SUBMESSAGE_FIELDS_RESOLVER={self.SUBMESSAGE_FIELDS_RESOLVER}\n"
            f"EXPANDED_MESSAGE_FIELDS_RESOLVER={self.EXPANDED_MESSAGE_FIELDS_RESOLVER}\n"
            f"MAX_PATH={self.MAX_PATH}\n"
            f"FORBIDDEN_CHARACTERS_IN_FILENAME={self.FORBIDDEN_CHARACTERS_IN_FILENAME}\n"
            f"FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO={self.FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO}\n"
        )
        return s

    def setup_resolvers(
        self,
        for_event: EventFieldResolver,
        for_message: MessageFieldResolver,
        for_submessage: SubMessageFieldResolver,
        for_expanded_message: ExpandedMessageFieldResolver,
    ) -> "TH2Config":
        """Use this to set up your custom resolvers.

        Args:
            for_event:
            for_message:
            for_submessage:
            for_expanded_message:

        Returns:
            self
        """
        self.EVENT_FIELDS_RESOLVER: EventFieldResolver = for_event
        self.MESSAGE_FIELDS_RESOLVER: MessageFieldResolver = for_message
        self.SUBMESSAGE_FIELDS_RESOLVER: SubMessageFieldResolver = for_submessage
        self.EXPANDED_MESSAGE_FIELDS_RESOLVER: ExpandedMessageFieldResolver = for_expanded_message
        self.efr = self.EVENT_FIELDS_RESOLVER
        self.mfr = self.MESSAGE_FIELDS_RESOLVER
        self.smfr = self.SUBMESSAGE_FIELDS_RESOLVER
        self.emfr = self.EXPANDED_MESSAGE_FIELDS_RESOLVER

        return self


options = TH2Config()
