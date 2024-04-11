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

import re
from copy import copy
from operator import itemgetter
from typing import List, Union
from tabulate import tabulate

from collections import namedtuple, defaultdict
import csv


def pars_arg(arg) -> str:  # noqa
    res = re.sub("[^0-9a-zA-Z]+", "_", arg)
    if res[0].isdigit():
        res = "n_" + res

    return res


def namedtuple_with_slice(name, args):  # noqa
    args_dict = {arg: pars_arg(arg) for arg in args}
    new_args = [pars_arg(arg) for arg in args]
    cls = namedtuple(name, new_args)  # TODO - we can have the same values!!!

    # TODO - I think we don't need getitem for strings. (strings column names.
    #  We would not do `row.abc` but we often have abc like 'a b 123 c' so it's not a problem.
    #  It means we don't need named tuples more
    #   We need to get only via item NOT ATTRIBUTE
    def getitem(self, index):
        # `type(self)` can result in issues in case of multiple inheritance.
        # But shouldn't be an issue here.
        if isinstance(index, int):
            value = super(type(self), self).__getitem__(
                index
            )  # Superclass for namedtuple is sequence
        elif isinstance(index, slice):
            value = super(type(self), self).__getitem__(index)
            cls = namedtuple(name, new_args[index])
            cls.__getitem__ = getitem
            value = cls(*value)
        elif isinstance(index, str):
            value = getattr(self, args_dict[index])
            # raise Exception('I dont can stings now')
        return value

    cls.__getitem__ = getitem
    return cls


class RowBase(tuple):
    _column_idx = {}  # {COL_NAME: index}

    def __new__(cls, *args: list):
        if not cls._column_idx:
            raise Exception("Row class is not initialized.")

        return super().__new__(cls, args)

    def __init__(self, *args: list):  # noqa
        if len(self._column_idx) != len(args):
            raise Exception(
                f"The number of provided values '{len(args)}' != the number of columns '{len(self._column_idx)}'"
            )
        super().__init__()

    @property
    def keys(self):
        return self._column_idx.keys()

    def _get_idx(self, col_name) -> int:
        try:
            return self._column_idx[col_name]
        except KeyError:
            raise Exception(f"Row class doesn't have '{col_name}' column")

    def __getitem__(self, index):
        # `type(self)` can result in issues in case of multiple inheritance.
        # But shouldn't be an issue here.
        if isinstance(index, int):
            value = super().__getitem__(index)
            # elif isinstance(index, slice):
        #     new_column_idx =
        #     value = self.__getitem__(index)
        #     cls = namedtuple(name, new_args[index])
        #     cls.__getitem__ = getitem
        #     value = cls(*value)
        elif isinstance(index, str):
            value = self[self._get_idx(index)]
        else:
            raise Exception("Some unexpected situation")

        return value


def row_cls_init(name, args):
    """Init RowBase."""
    cls = type(name, (RowBase,), {})
    cls._column_idx = {k: idx for idx, k in enumerate(args)}
    return cls


# TODO - this table should be placed to another repo in the future.
class PerfectTable:
    def __init__(self, header: List[str]):  # noqa
        self._headers = tuple(str(h) for h in header)
        self.row_class: RowBase = self._create_row_class(self._headers)
        self._rows = []
        self._columns = defaultdict(tuple)
        # self._add_headers_as_attr()

    def _create_row_class(self, headers) -> RowBase:
        # return namedtuple_with_slice("Row", headers)
        return row_cls_init("Row", headers)

    def __contains__(self, item):
        return item in self._headers

    def __iter__(self):
        return iter(self._rows)

    def __getitem__(self, item):
        if isinstance(item, int) or isinstance(item, slice):
            return self._rows[item]
        elif isinstance(item, str):
            return self.get_column(item)

    def __repr__(self):
        # use tabulate
        return tabulate(self.get_list_repr(), headers="firstrow", tablefmt="grid")

    def _repr_html_(self):
        # TODO - non zero and non None values we can highlight
        # FOR Jupyter
        return tabulate(self.get_list_repr(), headers="firstrow", tablefmt="html")

    # def _add_headers_as_attr(self):
    #     args_dict = {pars_arg(arg): arg
    #                  for arg in args}
    #     new_args = [pars_arg(arg) for arg in args]
    #     # TODO - doesn't work
    #     for h in self.header:
    #         prop = property(lambda self: self.get_column(h))  # self._create_prop_for_attrs(h)
    #         setattr(self, h, prop)

    def _check_columns_existence(self, columns):
        for c in columns:
            if c not in self.header:
                raise ValueError(f"Column '{c}' is not in the table columns: {self.header}")

    def get_list_repr(self):
        return [self.header, *self.rows]

    @classmethod
    def read_csv(self, path, strip=False):
        # TODO - check pandas name
        self._path = path

        with open(path, "r") as f_obj:
            reader = csv.reader(f_obj, delimiter=",")

            rows = tuple(
                row for row in reader
            )  # 'generator' object is not subscriptable  if generator

        self._headers = tuple(rows[0])
        self.row_class = self._create_row_class(self.header)
        x: list
        if strip:
            self._rows = [
                self.row_class(*[v.strip() for v in x if isinstance(v, str)]) for x in rows[1:]
            ]
        else:
            self._rows = [self.row_class(*x) for x in rows[1:]]

        # # TODO - I think it's worth initializing it lazily, on demand.
        # #   It someone requested the column, we should add it at this time
        # self._columns = defaultdict(tuple)
        # for idx, name in enumerate(self._headers):
        #     self._columns[name] = tuple(row[idx] for row in self._rows[1:])

        # Add headers as attributes.
        for h in self._headers:
            setattr(self, h, self._columns[h])

    def to_csv(self, path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self._headers)
            writer.writerows(self._rows)

    # @property
    # def path(self):
    #     """Returns the path to csv file."""
    #     return self._path

    def _create_prop_for_attrs(self, name):
        @property
        def get_col_prop(self):
            return self.get_column(name)

        return get_col_prop

    def get_column(self, name):
        # Lazy get by column.
        r = self._columns[name]
        if r:
            return r
        else:
            col_idx = self.header.index(name)
            self._columns[name] = tuple(row[col_idx] for row in self.rows)
            return self._columns[name]

    @property
    def header(self):
        """Returns a list of header names."""
        return self._headers

    @property
    def rows(self):
        """Returns a list of rows."""
        return self._rows

    def add_rows(self, rows):
        """Add rows to the table.

        Args:
            rows: rows of data, should be an iterable of lists, each list with as many
                elements as the table has fields
        """
        for row in rows:
            self.add_row(row)

    def _append_row(self, row: List):
        self._rows.append(self.row_class(*row))

    def add_row(self, row: List):
        """Add a row to the table.

        Args:
            row: row of data, should be a list with as many elements as the table
                has fields
        """
        if self.header and len(row) != len(self.header):
            raise ValueError(
                "Row has incorrect number of values, "
                f"(actual) {len(row)}!={len(self.header)} (expected)"
            )
        self._append_row(row)

    def filter(self, condition):
        """Returns new table. Not update current.

        Args:
            condition: any function with one argument Row. So you apply some filter to every Row.
                Row is the Row class.

        Returns:
            new Table

        Example:
            tbl.filter(lambda row: row['column_ABC'] == 'my string')

        """
        new = self.__class__(header=self.header)
        for row in self.rows:
            if condition(row):
                new.add_row(row)
        return new

    def sort_by(self, columns: Union[List[str], str], ascending=True):
        """Sort (updates the object) and returns self."""
        if isinstance(columns, str):
            columns = [columns]

        self._check_columns_existence(columns)

        s_rows = self.rows
        for sort_col in columns[::-1]:
            s_rows = sorted(s_rows, key=itemgetter(sort_col), reverse=not ascending)

        self._rows = s_rows

        return self

    def change_columns_order(self, columns_order: List[str]):
        self._check_columns_existence(columns_order)
        header_len = len(self.header)
        assert len(columns_order) == header_len

        # {col_name: idx} in the original table
        c_idxes = {c_name: self.header.index(c_name) for c_name in columns_order}

        new_header = columns_order
        orig_rows = copy(self.rows)
        self._headers = tuple(new_header)
        self._rows = []
        self.row_class = self._create_row_class(new_header)
        for row in orig_rows:
            self._append_row([row[c_idxes[column_name]] for column_name in columns_order])

        return self


if __name__ == "__main__":
    t = PerfectTable(["a", "b", "c"])
    t.add_rows(
        [
            (4, "c", 0),
            (3, "z", 1),
            (3, "a", 2),
            (3, "x", 3),
            (1, "b", 4),
        ]
    )

    print(t.sort_by(["a", "b", "c"]))
    # print(t.sort_by(['b', 'a']))
    print(t.change_columns_order(["b", "c", "a"]))
    print(t.sort_by("b", ascending=True))
    print(t.header)
    print(t["a"])
    print(t["b"])
    print(t["c"])
