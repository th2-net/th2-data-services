from typing import Dict, Union

from tabulate import tabulate


def calculate_stats_dict(data: Dict, sort_values: bool = False):
    table = [["category", "count"]]  # Header
    total = 0
    result = []
    for item in data.items():
        result.append([item[0], str(item[1])])
        total += item[1]

    if sort_values:
        result.sort(key=lambda item: int(item[1]), reverse=True)

    table.extend(result)
    table.append(["CATEGORIES", str(len(data))])
    table.append(["TOTAL", str(total)])
    return table


def print_stats_dict(
    data: Dict, return_html: bool = False, sort_values: bool = False, tabulate_style: str = "grid"
) -> Union[None, str]:
    """Prints Statistics.

    Args:
        data: Dictionary of data
        return_html: Return HTML format, defaults to False
        sort_values: Sort result, defaults to False
        tabulate_style: Table format style, defaults to "grid"

    Returns:
        None if return_html is False else str
    """
    table = calculate_stats_dict(data, sort_values)

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt=tabulate_style))
        return None


def print_measurement_dict(data: Dict, return_html: bool = False):
    """Prints Measurements.

    Args:
        data: Dictionary of data
        return_html: Return HTML format, defaults to False

    Returns:
        None if return_html is False else str
    """
    header = list(set(key for value in data.values() for key in value if key != "distr"))
    header.sort()
    table = [["category", *header]]

    for key, value in data.items():
        row = [key]
        for header_name in header:
            row.append(str(value[header_name]))
        table.append(row)

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
        return None