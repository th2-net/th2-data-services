from typing import Union, Iterable


class Filter:
    """The class that provides method of filters implementation URL of rpt-data-provider."""

    def __init__(self, name: str, values: Union[Iterable, str], negative: bool = False, conjunct: bool = False):
        """
        Args:
            name (str): register the filter by its name.
            values (Union[Iterable, str]): One str with filter value or list of filter values.
            negative (bool):  If true, will match events/messages that do not match those specified values.
                If false, will match the events/messages by their values. Defaults to false.
            conjunct (bool): If true, each of the specific filter values should be applied
                If false, at least one of the specific filter values must be applied
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
