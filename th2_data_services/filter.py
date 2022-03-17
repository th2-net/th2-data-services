from typing import Union, List, Tuple

from th2_grpc_data_provider.data_provider_template_pb2 import Filter as grpc_Filter, FilterName as grpc_FilterName
import google.protobuf.wrappers_pb2


class Filter:
    """The class for using rpt-data-provider filters API."""

    def __init__(
        self, name: str, values: Union[List[str], Tuple[str], str], negative: bool = False, conjunct: bool = False
    ):
        """Filter constructor.

        Args:
            name (str): Filter name.
            values (Union[List[str], Tuple[str], str]): One string with filter value or list of filter values.
            negative (bool):  If true, will match events/messages that do not match those specified values.
                If false, will match the events/messages by their values. Defaults to false.
            conjunct (bool): If true, each of the specific filter values should be applied
                If false, at least one of the specific filter values must be applied.
        """
        self.name = name

        if isinstance(values, (list, tuple)):
            self.values = map(str, values)
        else:
            self.values = [str(values)]

        self.negative = negative
        self.conjunct = conjunct

    def url(self) -> str:
        """Forms a filter.

        For help use this readme:
        https://github.com/th2-net/th2-rpt-data-provider#filters-api.

        Returns:
            str: Formed filter.
        """
        return (
            f"&filters={self.name}"
            + "".join([f"&{self.name}-values={val}" for val in self.values])
            + f"&{self.name}-negative={self.negative}"
        )

    def grpc(self) -> grpc_Filter:
        return grpc_Filter(
            name=grpc_FilterName(filter_name=self.name),
            negative=google.protobuf.wrappers_pb2.BoolValue(value=self.negative),
            values=self.values,
            conjunct=google.protobuf.wrappers_pb2.BoolValue(value=self.conjunct),
        )
