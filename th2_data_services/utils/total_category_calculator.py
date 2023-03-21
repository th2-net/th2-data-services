import time
from random import choice
from typing import List, Tuple, Union, Dict, Sequence, TypeVar
from prettytable import PrettyTable
from collections import Counter
import itertools

from th2_data_services.utils.aggregation_classes import TotalCategoryTable

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

class TotalCategoryCalculator:
    def __init__(self,
                 categories: List[Category],
                 combinations: Union[List[Sequence[str]], List[Sequence[Category]]]):
        """
        Calculates, aggregates to tables and prints categories combinations.

        This class allows you to calculate any metrics and their combinations in stream-like way.

        It does not accumulate all data in memory.
        Keeps calculated metrics only.

        categories: [Category('a'), Category(b)]
        combinations: e.g. [(a,),(a,b)].  You can put metric objects or metrics names.

        """
        self.metrics = categories
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
    sc = TotalCategoryCalculator(metrics_list, all_metrics_combinations)

    for m in messages:
        sc.append(m)

    sc.show()

    print(time.time() - t1)

    print(sc.get_table(['direction', 'messageType', session_m], add_total=True))
    print(time.time() - t1)
