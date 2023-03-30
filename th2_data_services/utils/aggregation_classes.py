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
from typing import List

from tabulate import tabulate

from th2_data_services.utils.perfect_table import PerfectTable


class AggrClassBase(ABC):
    @abstractmethod
    def _repr_html_(self):
        pass

    def __html__(self):
        self._repr_html_()

    def html_format(self):
        return self._repr_html_()


# TODO - if categorizer returns non-str but tuple or list or dict, we can provide more opportunities!
class EventStatTotalValue:
    def __init__(
        self,
        value,
    ):  # noqa
        self.value = value


# TODO - this is deprecated and should be removed. Use TotalCategoryTable instead
# TODO - Values of Categories should be objects with metainfo
#   So not only value = Cnt
#   But also status, and everything else
#   If we can such values, we can sort, and analyse them!
class CategoryTotal(dict[str, int], AggrClassBase):
    # service fields
    # TODO - configure fields order?

    # TODO
    #   1. now it sorts by count. What about status or category name?
    def __init__(self, val: dict[str, int]):
        """TODO - add.

        Args:
            val: add
        """
        super().__init__(val)

        self._table = []
        header = ["category", "count"]
        self._table.append(header)

        total = 0
        result = []
        for category_name, category_value in self.items():
            result.append([category_name, str(category_value)])
            total += category_value

        # if sort_values:
        #     result.sort(key=lambda item: int(item[1]), reverse=True)

        self._table.extend(result)
        self.categories_cnt = len(self.keys())  # Without total.
        self.total = total

        self._table.append(["CATEGORIES", str(self.categories_cnt)])
        self._table.append(["TOTAL", str(total)])

    def __repr__(self):
        return tabulate(self._table, headers="firstrow", tablefmt="grid")

    def _repr_html_(self):
        # TODO - non zero and non None values we can highlight
        # FOR Jupyter
        return tabulate(self._table, headers="firstrow", tablefmt="html")

    def get_categories(self) -> List[str]:
        """Returns categories."""
        return list(self.keys())

    # def sort_by(self, categories: List[str]):
    #     """Sort (update the object) and returns self."""
    #     return self

    # def show_format(self, **kwargs):
    #     return tabulate(self, **kwargs)


# TODO - this is deprecated and should be removed. Use  FrequencyCategoryTable
class CategoryFrequencies(list, AggrClassBase):
    def __repr__(self):
        return tabulate(self, headers="firstrow", tablefmt="grid")

    def _repr_html_(self):
        # TODO - non zero and non None values we can highlight
        # FOR Jupyter
        return tabulate(self, headers="firstrow", tablefmt="html")

    def show_format(self, **kwargs):
        return tabulate(self, **kwargs)

    def get_header(self) -> List[str]:
        """Returns header.

        First value is always timestamp.
        """
        return self[0]

    def get_categories(self) -> List[str]:
        """Returns categories."""
        return self.get_header()[1:]  # Skip timestamp.

    def by_category(self, name, exclude_zero_values=True):
        """Returns CategoryFrequencies for requested column."""
        header_lst = self.get_header()
        col_name_idx = header_lst.index(name)
        res = CategoryFrequencies()
        timestamp_col_name = header_lst[0]
        res.append([timestamp_col_name, name])
        for row in self[1:]:
            val = row[col_name_idx]
            if exclude_zero_values:
                if val != 0:
                    res.append([row[0], val])
            else:
                res.append([row[0], val])

        return res


# TODO -- new tables
#   They will change deprecated above


class CategoryTable(ABC, PerfectTable):
    def __init__(self, header: List[str]):  # noqa
        super().__init__(header)
        self._service_columns = {}  # {'col_name': 'idx'}
        self._service_rows = []  # [idx]


class FrequencyCategoryTable(CategoryTable):
    def __init__(self, header: List[str], rows=None):  # noqa
        super().__init__(header)
        self.service_columns = {
            "timestamp": 0,
        }  # {'col_name': 'idx'}
        if rows is not None:
            self.add_rows(rows)

    def get_categories(self) -> List[str]:
        """Returns categories."""
        return self.header[1:]  # Skip timestamp.

    def by_category(self, name, exclude_zero_values=True):
        """Returns CategoryFrequencies for requested column."""
        header_lst = self.header
        if name not in self.get_categories():
            raise ValueError(f"'{name}' is not categories: {self.get_categories()}")
        col_name_idx = header_lst.index(name)
        timestamp_col_name = header_lst[0]
        fct = FrequencyCategoryTable(header=[timestamp_col_name, name])

        for row in self.rows:
            val = row[col_name_idx]
            if exclude_zero_values:
                if val != 0:
                    fct.add_row([row[self.service_columns["timestamp"]], val])
            else:
                fct.add_row([row[self.service_columns["timestamp"]], val])

        return fct

    def by_categories(self, names: List[str], exclude_zero_values=True):
        """Returns CategoryFrequencies for requested column."""
        header_lst = self.header
        for name in names:
            if name not in self.get_categories():
                raise ValueError(f"'{name}' is not categories: {self.get_categories()}")

        col_name_idxs = []
        for name in names:
            col_name_idxs.append(header_lst.index(name))

        timestamp_col_name = header_lst[0]
        fct = FrequencyCategoryTable(header=[timestamp_col_name, *names])

        for row in self.rows:
            vals = [row[idx] for idx in col_name_idxs]
            if exclude_zero_values:
                if any(vals) != 0:
                    fct.add_row([row[self.service_columns["timestamp"]], *vals])
            else:
                fct.add_row([row[self.service_columns["timestamp"]], *vals])

        return fct


class TotalCategoryTable(CategoryTable):
    # This class allows to create tables with multiple categories. e.g  type | status | count
    def __init__(self, header, rows=None):  # noqa
        super().__init__(header)
        self.service_columns = {
            "timestamp": 0,
        }  # {'col_name': 'idx'}
        if rows is not None:
            self.add_rows(rows)

    @property
    def total(self):
        return sum(self["count"])

    def _totals_line(self):
        totals = []
        for col_name in self.header:
            col_tuple = self[col_name]

            try:
                # If all Bool.
                if all([isinstance(x, bool) for x in col_tuple]):
                    pos = sum(col_tuple)
                    neg = len(col_tuple) - pos
                    totals.append(f"{pos}/{neg}")
                else:
                    totals.append(sum(col_tuple))
            except:
                totals.append("")

        return totals

    def add_rows_from_dict(self, d: dict):
        result = []
        for category_name, category_value in d.items():
            result.append([category_name, str(category_value)])
            # total += category_value

        # if sort_values:
        #     result.sort(key=lambda item: int(item[1]), reverse=True)

        self.add_rows(result)

    # TODO - I'm not sure that it's categories!
    def get_categories(self) -> List:
        return [row[:-1] for row in self.rows]

    def get_list_repr(self):
        additional_rows = [
            # ['' for i in range(len(self.header) - 1)] + [self.total],
            ["count"] + ["" for _ in range(len(self.header) - 1)] + [len(self.rows)],
            ["totals"] + self._totals_line(),
        ]
        return [[" "] + list(self.header), *[[" "] + list(row) for row in self.rows], *additional_rows]
