import time
from abc import ABC, abstractmethod
from random import choice
from typing import Literal, Optional, List, Tuple, Union, Dict, Sequence, TypeVar
from prettytable import PrettyTable
import json
from collections import Counter
import itertools
from th2_data_services.utils.perfect_table import PerfectTable

"""
Положим есть 3 метрики
A, B, C

A бывае In, Out

B - любое значение

C - тоже любое

Нужно сформировать комбинации

A
AB
AC

B
BC

C

ABC

Порядок влияет только на отображение.

пример
1. A: in, B: 0, C: x

a += 1
ab = {in/0: +=1}


"""


class CategoryTable(ABC, PerfectTable):
    def __init__(self, header: List[str]):
        super().__init__(header)
        self._service_columns = {}  # {'col_name': 'idx'}
        self._service_rows = []  # [idx]


# class CategoryTable(ABC):
#     def __init__(self, header, rows=None):
#         self._service_columns = {}  # {'col_name': 'idx'}
#         self._service_rows = []  # [idx]
#         self._table = PrettyTable(field_names=header)
#         if rows is not None:
#             self.add_rows(rows)
#
#     def __repr__(self):
#         return self._table.get_string()
#
#     def _repr_html_(self):
#         # TODO - non zero and non None values we can highlight
#         # FOR Jupyter
#         return self._table.get_html_string()
#
#     def __getitem__(self, index):
#         t = self._table.__getitem__(index)
#         new = CategoryTable(header=t.field_names, rows=t.rows)
#         return new
#
#     def _new_class_from_the_table(self, table: PrettyTable):
#         return self.__class__(header=table.field_names, rows=table.rows)
#
#     # def show_format(self, **kwargs):
#     #     return tabulate(self, **kwargs)
#
#     def add_rows(self, rows):
#         self._table.add_rows(rows)
#
#     def add_row(self, row):
#         self._table.add_row(row)
#
#     def get_rows(self) -> List[list]:
#         return self._table.rows
#
#     def convert_to_list(self):
#         # list representation
#         pass
#
#     def get_header(self) -> List[str]:
#         """Returns header.
#
#         First value is always timestamp.
#         """
#         return self._table.field_names
#
#     @abstractmethod
#     def get_categories(self) -> List[str]:
#         """Returns categories."""
#         pass
#
#     # def by_category(self, name, exclude_zero_values=True):
#     #     """Returns CategoryFrequencies for requested column."""
#     #     header_lst = self.get_header()
#     #     col_name_idx = header_lst.index(name)
#     #     res = CategoryTable()
#     #     timestamp_col_name = header_lst[0]
#     #     res.append([timestamp_col_name, name])
#     #     for row in self[1:]:
#     #         val = row[col_name_idx]
#     #         if exclude_zero_values:
#     #             if val != 0:
#     #                 res.append([row[0], val])
#     #         else:
#     #             res.append([row[0], val])
#     #
#     #     return res
#
#     def sort_by(self, columns: List[str]):
#         """Sort (update the object) and returns self."""
#         return self
#
#     def _check_columns_existence(self, columns):
#         for c in columns:
#             if c not in self.get_header():
#                 raise ValueError(f"column '{c}' is not in the table columns: {self.get_header()}")
#
#     # def get_column(self, name):
#     #     col_index = self.get_header().index(name)
#     #     for row in self.get_rows():
#     #         res. row[col_index]
#
#     def order_by(self, columns: List[str]):
#         # TODO - in progress
#         self._check_columns_existence(columns)
#         c_idxes = {c_name: self.get_header().index(c_name) for c_name in columns}
#         # new_header =
#         self._table.del_column()
#         return self
#
#     # TODO - I want to see here where cnt > 1
#     def filter(self, condition):
#         """Returns new table. Not update current
#
#         Args:
#             condition:
#
#         Returns:
#
#         """
#         new = self.__class__(header=self.get_header())
#         for row in self.get_rows():
#             if condition(row):
#                 new.add_row(row)
#         return new


# class TotalCategoryTable(CategoryTable):
#     # Хочу сложные категории type | status | count
#     # Но как тогда по категории значение получать?
#     def __init__(self, header, rows=None):
#         super().__init__(header, rows)
#         self.service_columns = {
#             "timestamp": 0,
#         }  # {'col_name': 'idx'}
#
#     # TODO - add as an option add_total
#
#     def add_rows_from_dict(self, d: dict):
#         result = []
#         for category_name, category_value in d.items():
#             result.append([category_name, str(category_value)])
#             # total += category_value
#
#         # if sort_values:
#         #     result.sort(key=lambda item: int(item[1]), reverse=True)
#
#         self.add_rows(result)
#
#     def get_categories(self) -> List:
#         return [row[:-1] for row in self.get_rows()]
#
#     def get_total(self):
#         pass


# class FrequencyCategoryTable(CategoryTable):
#     def __init__(self, header, rows=None):
#         super().__init__(header, rows)
#         self.service_columns = {
#             "timestamp": 0,
#         }  # {'col_name': 'idx'}
#
#     def get_categories(self) -> List[str]:
#         """Returns categories."""
#         return self.get_header()[1:]  # Skip timestamp.
#
#     def by_category(self, name, exclude_zero_values=True):
#         """Returns CategoryFrequencies for requested column."""
#         header_lst = self.get_header()
#         if name not in self.get_categories():
#             raise ValueError(f"'{name}' is not categories: {self.get_categories()}")
#         col_name_idx = header_lst.index(name)
#         timestamp_col_name = header_lst[0]
#         fct = FrequencyCategoryTable(header=[timestamp_col_name, name])
#
#         for row in self.get_rows():
#             val = row[col_name_idx]
#             if exclude_zero_values:
#                 if val != 0:
#                     fct.add_row([row[self.service_columns['timestamp']], val])
#             else:
#                 fct.add_row([row[self.service_columns['timestamp']], val])
#
#         return fct


class FrequencyCategoryTable(CategoryTable):
    def __init__(self, header: List[str], rows=None):
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
                    fct.add_row([row[self.service_columns['timestamp']], val])
            else:
                fct.add_row([row[self.service_columns['timestamp']], val])

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
                    fct.add_row([row[self.service_columns['timestamp']],  *vals])
            else:
                fct.add_row([row[self.service_columns['timestamp']], *vals])

        return fct


class TotalCategoryTable(CategoryTable):
    # Хочу сложные категории type | status | count
    # Но как тогда по категории значение получать?
    def __init__(self, header, rows=None):
        super().__init__(header)
        self.service_columns = {
            "timestamp": 0,
        }  # {'col_name': 'idx'}
        if rows is not None:
            self.add_rows(rows)

    # TODO - add as an option add_total

    @property
    def total(self):
        return sum(self['count'])


    def _totals_line(self):
        totals = []
        for col_name in self.header:
            try:
                totals.append(sum(self[col_name]))
            except:
                totals.append('')

        return totals

    def add_rows_from_dict(self, d: dict):
        result = []
        for category_name, category_value in d.items():
            result.append([category_name, str(category_value)])
            # total += category_value

        # if sort_values:
        #     result.sort(key=lambda item: int(item[1]), reverse=True)

        self.add_rows(result)

    def get_categories(self) -> List:
        return [row[:-1] for row in self.rows]

    def get_list_repr(self):
        additional_rows = [
            # ['' for i in range(len(self.header) - 1)] + [self.total],
            ['count'] + ['' for _ in range(len(self.header)-1)] + [len(self.rows)] ,
            ['totals']+self._totals_line(),
        ]
        return [[' ']+list(self.header), *[[' ']+list(row) for row in self.rows], *additional_rows]


class Category:
    def __init__(self, name: str, get_func):
        self.name: str = name
        self.get_func = get_func

    def __repr__(self):
        return f"Category<{self.name}>"


CategoryCombination = TypeVar('CategoryCombination', Sequence[str], Sequence[Category])


def get_all_metric_combinations(metrics: Union[List[str], List[Category]]):
    """Returns all combinations of provided metrics."""
    metric_combinations = []

    for L in range(len(metrics) + 1):
        for subset in itertools.combinations(metrics, L):
            if subset:
                metric_combinations.append(subset)

    return metric_combinations


# Сначала нужно все метрики вытаскивать, а только потом соединять

# МОжно использовтаь как аналог, для get_category_totals
class CategoryTotalCalculator:
    def __init__(self,
                 metrics: List[Category],
                 combinations: Union[List[Sequence[str]], List[Sequence[Category]]]):
        """
        Calculate, aggregate to tables and print metrics combinations.

        This class allows you to calculate any metrics and their combinations in stream-like way.

        It does not accumulate all data in memory.
        Keeps calculated metrics only.

        metrics: [Metric('a'), Metric(b)]
        combinations: e.g. [(a,),(a,b)].  You can put metric objects or metrics names.

        """
        self.metrics = metrics
        self.combinations: List[Tuple[str]] = []

        metric: Category
        for comb in combinations:
            new_comb = self._prepare_combination(comb)
            self.combinations.append(new_comb)

        self.counter_field_name = 'count'
        self._counters: Dict[Tuple[str], Counter] = {}

        for v in self.combinations:
            self._counters[v] = Counter()

    def _get_counter(self, combination: Tuple[str]) -> Counter:
        """Returns counter for the combination.

        Expects prepared combination (after _prepare_combination method).
        """
        try:
            return self._counters[combination]
        except KeyError:
            raise Exception(
                f"Unknown combination. The following combination '{combination}' is not provided to constructor.")

    def _prepare_combination(self, combination: CategoryCombination) -> Tuple[str]:
        """Returns combination in the required view."""
        new_comb = []
        for cv in combination:
            if isinstance(cv, str):
                new_comb.append(cv)
            elif isinstance(cv, Category):
                new_comb.append(cv.name)
            else:
                raise ValueError(f'Unexpected combination value, {combination}')

        new_comb.sort()  # Because ABC == CAB == BAC == CBA ...

        return tuple(new_comb)

    def handle_objects(self, objects):
        for o in objects:
            self.append(o)

    # TODO - хорошо, что у нас есть такое, а не сразу все сообщения крутит внутри.
    #   т.к. get_category_totals_p  принимает 1 элемент, для того, чтобы можно было итерировать в
    #   итератор процессорах.!!
    def append(self, m: dict):
        """Put some object to take it into account."""
        metric_values = {}
        for metric in self.metrics:
            metric_values[metric.name] = metric.get_func(m)

        # concat them  == values

        for v in self.combinations:  # v = ['session', 'direction']
            val_for_counter = tuple([metric_values[metric] for metric in v])
            self._counters[v].update([val_for_counter])

    def get_table(self, combination: CategoryCombination, add_total=False) -> TotalCategoryTable:
        """Returns a PrettyTable class for certain combination.

        Args:
            combination: Union[Tuple[str], List[str]]
            add_total: If True, adds total value in the last line.

        """
        combination = self._prepare_combination(combination)

        t = PrettyTable()
        t.field_names = [*combination, self.counter_field_name]
        c = self._get_counter(combination)

        if add_total:
            total_val = 0

            for key, cnt in c.items():
                t.add_row([*key, cnt])
                total_val += cnt

            # Add total row.
            t.add_row([*['' for _ in combination], total_val])

        else:
            for key, cnt in c.items():
                t.add_row([*key, cnt])

        return TotalCategoryTable(header=t.field_names, rows=t.rows).sort_by([self.counter_field_name], ascending=False)

    def show(self):
        """Prints all tables.

        Sorted by cnt.
        """
        for combination in self.combinations:
            t = self.get_table(combination)
            t.reversesort = True
            t.sortby = self.counter_field_name
            print(t)


if __name__ == '__main__':
    messages = []
    for i in range(1_000):
        dir = choice(['IN', 'OUT'])
        session = choice(['s1', 's2', 's3', 's4'])
        messageType = choice(['NewOrderSingle', 'Cancel', 'Amend'])
        messages.append({'direction': dir, 'sessionId': session, 'messageType': messageType})

    t1 = time.time()
    direction_m = Category('direction', lambda m: m['direction'])
    session_m = Category('session', lambda m: m['sessionId'])
    message_type_m = Category('messageType', lambda m: m['messageType'])

    metrics_list = [
        direction_m,
        session_m,
        message_type_m,
    ]

    all_metrics_combinations = get_all_metric_combinations(metrics_list)
    print(all_metrics_combinations)
    sc = CategoryTotalCalculator(metrics_list, all_metrics_combinations)

    for m in messages:
        sc.append(m)

    sc.show()

    print(time.time() - t1)

    print(sc.get_table(['direction', 'messageType', session_m], add_total=True))
    print(time.time() - t1)
