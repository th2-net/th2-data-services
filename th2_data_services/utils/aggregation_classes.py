from abc import ABC, abstractmethod
from typing import List

from tabulate import tabulate


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
    def __init__(self, value, ):
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
