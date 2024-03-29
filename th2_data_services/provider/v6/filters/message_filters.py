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

from th2_data_services.provider.v6.filters.filter import Provider6MessageFilter


class TypeFilter(Provider6MessageFilter):
    """Will match the messages by their full type name."""

    FILTER_NAME = "type"


class BodyBinaryFilter(Provider6MessageFilter):
    """Will match the messages by their binary body."""

    FILTER_NAME = "bodyBinary"


class BodyFilter(Provider6MessageFilter):
    """Will match the messages by their parsed body."""

    FILTER_NAME = "body"


class AttachedEventIdsFilter(Provider6MessageFilter):
    """Filters the messages that are linked to the specified event id."""

    FILTER_NAME = "attachedEventIds"
