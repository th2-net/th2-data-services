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
from abc import ABC, abstractmethod


class EventFieldsResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_id(event):
        pass

    @staticmethod
    @abstractmethod
    def get_parent_id(event):
        pass

    @staticmethod
    @abstractmethod
    def get_status(event):
        pass

    @staticmethod
    @abstractmethod
    def get_name(event):
        pass

    @staticmethod
    @abstractmethod
    def get_batch_id(event):
        pass

    @staticmethod
    @abstractmethod
    def get_is_batched(event):
        pass

    @staticmethod
    @abstractmethod
    def get_type(event):
        pass

    @staticmethod
    @abstractmethod
    def get_start_timestamp(event):
        pass

    @staticmethod
    @abstractmethod
    def get_end_timestamp(event):
        pass

    @staticmethod
    @abstractmethod
    def get_attached_messages_ids(event):
        pass

    @staticmethod
    @abstractmethod
    def get_body(event):
        pass


class MessageFieldsResolver(ABC):
    @staticmethod
    @abstractmethod
    def get_direction(message):
        pass

    @staticmethod
    @abstractmethod
    def get_session_id(message):
        pass

    @staticmethod
    @abstractmethod
    def get_type(message):
        pass

    @staticmethod
    @abstractmethod
    def get_connection_id(message):
        pass

    @staticmethod
    @abstractmethod
    def get_session_alias(message):
        pass

    @staticmethod
    @abstractmethod
    def get_subsequence(message):
        pass

    @staticmethod
    @abstractmethod
    def get_sequence(message):
        pass

    @staticmethod
    @abstractmethod
    def get_timestamp(message):
        pass

    @staticmethod
    @abstractmethod
    def get_body(message):
        pass

    @staticmethod
    @abstractmethod
    def get_body_base64(message):
        pass

    @staticmethod
    @abstractmethod
    def get_id(message):
        pass

    @staticmethod
    @abstractmethod
    def get_attached_event_ids(message):
        pass

    @staticmethod
    @abstractmethod
    def get_fields(message):
        pass
