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

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

"""
The idea of using resolvers:
    It solves the problem of having a few DataSources with the same data,
    but with different ways to get it.

    These classes provide you getter methods.
    Using these classes allows you to freely switch between different data
    formats and don't change your code.

    Resolvers solve the problem of data-format migration.
        - fields place can be changed
        - fields names can be changed

    Resolvers can work only with one event/message.
    It means, if your message has sub-messages it won't work, because resolver will not
    know with which sub-message should it work.

Implementation advice:
    1. raise NotImplementedError -- if your Implementation doesn't support this getter.

Performance impact:
    It a bit slower than using naked field access `dict['key']`.

    Data len: 2521467
    Every test has 10 takes of field. It means that the total number of them: 25214670

    get_and_return_10_fields_directly
    Total time taken in :  test_iterate 14.274808883666992  ~ 1766970
    get_and_return_10_fields_by_resolvers
    Total time taken in :  test_iterate 16.307125568389893  ~ 1546912
    DIRECT LwdpEventFieldsResolver get_and_return_10_fields_by_direct_resolvers
    Total time taken in :  test_iterate 16.423101902008057  ~ 1546912
    Via http_event_struct get_and_return_10_fields_via_http_event_struct
    Total time taken in :  test_iterate 14.83995270729065   ~ 1700247
"""


class EventFieldResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_id(event) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_parent_id(event) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_status(event) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_name(event) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_batch_id(event) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_is_batched(event) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def get_type(event) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_start_timestamp(event) -> Dict[str, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_end_timestamp(event) -> Dict[str, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_attached_messages_ids(event) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def get_body(event) -> Any:
        pass


class MessageFieldResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_direction(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_session_id(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_type(message) -> str:
        """This field was removed since LwDP3.

        Don't use it in new scripts.
        """

    @staticmethod
    @abstractmethod
    def get_sequence(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_timestamp(message) -> Dict[str, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_body(message) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        pass

    @staticmethod
    @abstractmethod
    def get_body_base64(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_id(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_attached_event_ids(message) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def expand_message(message) -> List[Dict[str, Any]]:
        """Extract a compounded message into a list of individual messages.

        Use it with `data.map_yield` instead of `data.map`.

        Warnings:
            expand_message function is not backward-compatible.
            If you use it in your scripts, there is no guarantee that everything
            will work if you change data-source because different data-sources
            have different messages structure.

        Args:
            message: Th2Message

        Returns:
            Iterable[Th2Message]
        """


class SubMessageFieldResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_subsequence(message) -> List[int]:
        pass

    @staticmethod
    @abstractmethod
    def get_type(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_fields(message) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def get_metadata(message) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def get_protocol(message) -> str:
        pass


class ExpandedMessageFieldResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_direction(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_session_id(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_type(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_sequence(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_timestamp(message) -> Dict[str, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_body(message) -> Union[Dict[str, Any]]:
        pass

    @staticmethod
    @abstractmethod
    def get_body_base64(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_id(message) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_attached_event_ids(message) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def get_subsequence(message) -> List[int]:
        pass

    @staticmethod
    @abstractmethod
    def get_fields(message) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def get_metadata(message) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def get_protocol(message) -> str:
        pass


# TODO - should be remove during release.
MessageFieldsResolver = MessageFieldResolver  # For backward compatibility.
# TODO - should be remove during release.
EventFieldsResolver = EventFieldResolver  # For backward compatibility.
