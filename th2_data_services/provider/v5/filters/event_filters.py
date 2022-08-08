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

from th2_data_services.provider.v5.filters.filter import Provider5EventFilter


class TypeFilter(Provider5EventFilter):
    """Will match the events which type contains one of the given substrings."""

    FILTER_NAME = "type"


class NameFilter(Provider5EventFilter):
    """Will match the events which name contains one of the given substrings."""

    FILTER_NAME = "name"


class BodyFilter(Provider5EventFilter):
    """Will match the events which body contains one of the given substrings."""

    FILTER_NAME = "body"


class AttachedMessageIdFilter(Provider5EventFilter):
    """Filters the events that are linked to the specified message id."""

    FILTER_NAME = "attachedMessageId"


class _StatusFilter(Provider5EventFilter):
    FILTER_NAME = "status"

    def url(self) -> str:
        """Generates the filter part of the HTTP protocol API.

        For help use this readme:
        https://github.com/th2-net/th2-rpt-data-provider#filters-api.

        Returns:
            str: Generated filter.
        """
        return f"&filters={self.name}" + "".join([f"&{self.name}-values={val}" for val in self.values])


class PassedStatusFilter(_StatusFilter):
    """Will match the events which status equals passed."""

    def __init__(self):  # noqa: D107
        super().__init__("passed")


class FailedStatusFilter(_StatusFilter):
    """Will match the events which status equals failed."""

    def __init__(self):  # noqa: D107
        super().__init__("failed")
