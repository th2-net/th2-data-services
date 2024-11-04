#  Copyright 2022-2024 Exactpro (Exactpro Systems Limited)
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
from typing import List


class IStub(ABC):
    class RequiredField:
        """This class used for mark required fields in your template."""

    REQUIRED_FIELD = RequiredField()

    def __init__(self):
        """Stab interface."""
        self._required_fields: list = self._define_required_fields()

    def _define_required_fields(self) -> List[str]:
        req_fields = []
        for k, v in self.template.items():
            if v is self.REQUIRED_FIELD:
                req_fields.append(k)

        return req_fields

    def _check_req_fields(self, fields):
        for rf in self._required_fields:
            if rf not in fields:
                raise TypeError(
                    f"Required field '{rf}' is absent in changed fields list ({fields})"
                )

    def _build_by_template(self, fields: dict) -> dict:
        """Builds new dict by template.

        All keys will be overwrited by fields.
        New keys from fields will be added to stub.

        Args:
            fields:

        Returns:
            Stub Dict

        """
        template = self.template.copy()
        for k, v in fields.items():
            template[k] = v
        return template

    def build(self, fields: dict) -> dict:
        """Builds a stub by template.

        All keys will be overwrited by fields.
        New keys from fields will be added to stub.

        Args:
            fields: Fields that will overwrite template.

        Returns:
            Stub dict.

        Raises:
            TypeError: If required fields is absent in changed fields list.
        """
        self._check_req_fields(fields)
        return self._build_by_template(fields)

    @property
    @abstractmethod
    def template(self) -> dict:
        pass


class IEventStub(IStub):
    """Just to mark Event Stub class."""

    def __repr__(self):
        return self.__class__.__name__


class IMessageStub(IStub):
    """Just to mark Message Stub class."""

    def __repr__(self):
        return self.__class__.__name__
