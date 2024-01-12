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

import time
from random import choice
from typing import List, Tuple, Union, Dict, Sequence, TypeVar
from prettytable import PrettyTable
from collections import Counter
import itertools

from th2_data_services.utils.aggregation_classes import TotalCategoryTable
from th2_data_services.utils.category import Category

"""
Suppose there are 3 metrics
A, B, C

A happens In, Out

B - any value

C - also any

Combinations need to be made.

A
AB
AC

B
BC

C

ABC

The order affects only the display.

example
1. A: in, B: 0, C: x

a += 1
ab = {in/0: +=1}


"""

CategoryCombination = TypeVar("CategoryCombination", Sequence[str], Sequence[Category])


def get_all_metric_combinations(metrics: Union[List[str], List[Category]]):
    """Returns all combinations of provided metrics."""
    metric_combinations = []

    for L in range(len(metrics) + 1):
        for subset in itertools.combinations(metrics, L):
            if subset:
                metric_combinations.append(subset)

    return metric_combinations


# First you need to pull out all the metrics, and only then connect


class TotalCategoryCalculator:
    def __init__(
        self,
        categories: List[Category],
        combinations: Union[List[Sequence[str]], List[Sequence[Category]]],
    ):
        """Calculates, aggregates to tables and prints categories combinations.

        This class allows you to calculate any metrics and their combinations in stream-like way.
        It calculates how many times do we met some combination of tags.

        It does not accumulate all data in memory.
        Keeps calculated metrics only.

        categories: [Category('a'), Category(b)]
        combinations: e.g. [(a,),(a,b)].  You can put metric objects or metrics names.

        """
        assert isinstance(categories, list)
        self.metrics = categories
        self.combinations: List[Tuple[str]] = []

        metric: Category
        for comb in combinations:
            new_comb = self._prepare_combination(comb)
            self.combinations.append(new_comb)

        self.counter_field_name = "count"
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
                f"Unknown combination. The following combination '{combination}' is not provided to constructor."
            )

    def _prep_combination_keep_order(self, combination: CategoryCombination) -> List[str]:
        """Returns combination in the required view."""
        new_comb = []
        for cv in combination:
            if isinstance(cv, str):
                new_comb.append(cv)
            elif isinstance(cv, Category):
                new_comb.append(cv.name)
            else:
                raise ValueError(f"Unexpected combination value, {combination}")

        return new_comb

    def _prepare_combination(self, combination: CategoryCombination) -> Tuple[str]:
        """Returns combination in the required view."""
        new_comb = []
        for cv in combination:
            if isinstance(cv, str):
                new_comb.append(cv)
            elif isinstance(cv, Category):
                new_comb.append(cv.name)
            else:
                raise ValueError(f"Unexpected combination value, {combination}")

        new_comb.sort()  # Because ABC == CAB == BAC == CBA ...

        return tuple(new_comb)

    def handle_objects(self, objects):
        for o in objects:
            self.append(o)

    # TODO - it's good that we have this, and not immediately all the messages are twisted inside.
    #   because get_category_totals_p takes 1 element, in order to be able to iterate over
    #   iterator processors.!!
    def append(self, m: dict):
        """Put some object to take it into account."""
        metric_values = {}
        for metric in self.metrics:
            metric_values[metric.name] = metric.get_func(m)

        # concat them  == values

        for v in self.combinations:  # v = ['session', 'direction']
            val_for_counter = tuple([metric_values[metric] for metric in v])
            self._counters[v].update([val_for_counter])

    def get_table(self, combination: CategoryCombination) -> TotalCategoryTable:
        """Returns a TotalCategoryTable class for certain combination.

        Args:
            combination: Union[Tuple[str], List[str]]

        Returns:
            TotalCategoryTable

        """
        orig_comb = combination
        comb: Category
        orig_columns_order = self._prep_combination_keep_order(orig_comb)
        orig_columns_order.append(self.counter_field_name)

        combination = self._prepare_combination(combination)

        t = PrettyTable()
        t.field_names = [*combination, self.counter_field_name]
        counter = self._get_counter(combination)  # The object with calculated combinations.

        for key, cnt in counter.items():
            t.add_row([*key, cnt])

        return (
            TotalCategoryTable(header=t.field_names, rows=t.rows)
            .change_columns_order(orig_columns_order)
            .sort_by([self.counter_field_name], ascending=False)
        )

    def show(self):
        """Prints all tables.

        Sorted by cnt.
        """
        for combination in self.combinations:
            t = self.get_table(combination)
            t.reversesort = True
            t.sortby = self.counter_field_name
            print(t)


if __name__ == "__main__":
    messages = []
    for i in range(1_000):
        dir = choice(["IN", "OUT"])
        session = choice(["s1", "s2", "s3", "s4"])
        session = choice(["2023-05-04", "2023-04-03", "2023-05-03", "2023-05-12"])
        messageType = choice(["NewOrderSingle", "Cancel", "Amend"])
        messages.append({"direction": dir, "sessionId": session, "messageType": messageType})

    t1 = time.time()
    direction_m = Category("direction", lambda m: m["direction"])
    session_m = Category("session", lambda m: m["sessionId"])
    message_type_m = Category("messageType", lambda m: m["messageType"])

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
    tbl = sc.get_table(["direction", "messageType", session_m])
    print(tbl)
    print(tbl.transpose_column("session"))
    print(time.time() - t1)
