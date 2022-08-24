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
from importlib_metadata import version
from typing import Sequence, Union
from warnings import warn

v = version("th2_grpc_data_provider")

if v == "1.1.0":  # v6
    from th2_data_services.provider.v6.filters.filter import Provider6Filter as ProviderFilter  # noqa
elif v == "0.1.6":  # v5
    from th2_data_services.provider.v5.filters.filter import Provider5Filter as ProviderFilter  # noqa


class Filter(ProviderFilter):
    """The class for using rpt-data-provider filters API."""

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
        warn(
            f"{self.__class__.__name__} is deprecated. Use Filters of certain DataSource instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(name=name, values=values, negative=negative, conjunct=conjunct)
