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

from th2_data_services.provider.interfaces.filter import IProviderFilter
from typing import Sequence, Any, Union

from th2_grpc_data_provider.data_provider_pb2 import Filter as grpc_Filter, FilterName as grpc_FilterName
import google.protobuf.wrappers_pb2


class Provider6Filter(IProviderFilter):
    """General interface for Filters of Provider v6."""

    def __init__(
        self,
        name: str,
        values: Union[str, int, float, Sequence[Union[str, int, float]]],
        negative: bool = False,
        conjunct: bool = False,
    ):
        """Filter constructor.

        Args:
            name (str): Filter name.
            values (Union[str, int, float, Sequence[Union[str, int, float]]]): One string with filter value or list of filter values.
            negative (bool):  If true, will match events/messages that do not match those specified values.
                If false, will match the events/messages by their values. Defaults to false.
            conjunct (bool): If true, each of the specific filter values should be applied
                If false, at least one of the specific filter values must be applied.
        """
        self.name = name

        if isinstance(values, (list, tuple)):
            self.values = [str(v) for v in values]
        else:
            self.values = [str(values)]

        self.negative = negative
        self.conjunct = conjunct

    def __repr__(self):
        class_name = self.__class__.__name__
        return (
            f"{class_name}("
            f"name='{self.name}', "
            f"values={self.values}, "
            f"negative='{self.negative}', "
            f"conjunct='{self.conjunct}')"
        )

    def url(self) -> str:
        """Generates the filter part of the HTTP protocol API.

        For help use this readme:
        https://github.com/th2-net/th2-rpt-data-provider#filters-api.

        Returns:
            str: Generated filter.
        """
        return (
            f"&filters={self.name}"
            + "".join([f"&{self.name}-values={val}" for val in self.values])
            + f"&{self.name}-negative={self.negative}"
            + f"&{self.name}-conjunct={self.conjunct}"
        )

    def grpc(self) -> grpc_Filter:
        """Generates the grpc object of the GRPC protocol API."""
        return grpc_Filter(
            name=grpc_FilterName(name=self.name),
            negative=google.protobuf.wrappers_pb2.BoolValue(value=self.negative),
            value=self.values,
            conjunct=google.protobuf.wrappers_pb2.BoolValue(value=self.conjunct),
        )


class _Provider6FilterBase(Provider6Filter):
    FILTER_NAME = "FILTER_NAME"

    def __init__(self, values: Sequence[Any], negative: bool = False, conjunct: bool = False):
        super().__init__(self.FILTER_NAME, values, negative, conjunct)


class Provider6EventFilter(_Provider6FilterBase):
    """Base class for Event Filters of Provider v5."""


class Provider6MessageFilter(_Provider6FilterBase):
    """Base class for Message Filters of Provider v5."""
