import plotly.graph_objects as go
import vaex

from collections import defaultdict
from functools import reduce
from itertools import cycle, chain
from re import sub, search
from typing import Iterable, Union, List, Any, DefaultDict, Dict, Optional, Tuple
from IPython.core.display import display_html
from pandas import DataFrame, concat, Grouper, Series
from pandas.core.groupby import DataFrameGroupBy


def aggregate_by_groups(
    data: Union[Iterable[dict], DataFrame],
    *fields: str,
    total_row: bool = False,
    pivot: Union[Iterable[str], str] = None,
) -> Union[DataFrame, DataFrameGroupBy]:
    """Aggregates by fields.

    :param data: Data.
    :param fields: Fields for aggregate.
    :param total_row: Adding a total row.
    :param pivot: Which columns must is pivoted.
    :return: Statistics.
    """
    df = DataFrame(data)
    if df.empty:
        raise ValueError("Input data is empty.")
    if not fields:
        raise ValueError("Fields is empty.")

    df: DataFrame = (
        vaex.from_pandas(df)
        .groupby(by=fields, agg="count", sort=True)
        .to_pandas_df()
        .set_index([*fields])
    )

    if pivot:
        if isinstance(pivot, str):
            pivot = (pivot,)
        index = (field for field in fields if field not in pivot)
        df = df.reset_index().pivot(index=index, columns=pivot, values="count")
    if total_row:
        index_length = len(df.index.names)
        name = ("Total",) * index_length if index_length > 1 else "Total"
        df.loc[name, :] = [
            column.sum() if str(column.dtype) != "object" else "Total"
            for _, column in df.items()
        ]
    return df


def aggregate_by_intervals(
    data: Iterable[dict],
    time_field: str,
    agg: str = "count",
    resolution: str = "D",
    every: int = 1,
) -> DataFrame:
    """Aggregates by time. Lazy method.

    :param data: Data.
    :param time_field: Time field.
    :param agg: Aggregate function name.
    :param resolution: Datetime suffix for intervals.
    :param every: Frequently of intervals.
    :return: Show all groups in dataframe.
    """
    if not data:
        raise ValueError("Input data is empty.")

    dfv = vaex.from_pandas(DataFrame(data))
    compute = dfv.groupby(
        by=vaex.BinnerTime(
            expression=time_field, df=dfv, resolution=resolution, every=every
        ),
        agg=agg,
    ).to_pandas_df()

    return compute


def aggregate_several_group(
    data: Iterable[dict], display_html_df: bool = True, receive_df: bool = False
) -> Optional[DataFrame]:
    """Aggregates all groups in dataframe.

    :param data: Data.
    :param display_html_df: Whether display to html.
    :param receive_df: Whether to create dataframe.
    :return: Show all groups in dataframe.
    """

    if not data:
        raise ValueError("Input data is empty.")

    data = DataFrame(data)

    results = []
    for column in data.columns:
        results.append(aggregate_by_groups(data, column, total_row=True).reset_index())

    if display_html_df:
        html_str = ""
        for output, title in zip(results, chain(cycle([""]), cycle(["</br>"]))):
            html_str += '<th style="text-align: center"><td style="vertical-align:top">'
            html_str += f"<h2>{title}<h2>"
            html_str += output.to_html().replace(
                "table", 'table style="display:inline"'
            )
            html_str += "</td><th>"
        display_html(html_str, raw=True)

    if receive_df:
        result = reduce(
            lambda df, another_df: concat([df, another_df], axis=1)
            if len(df.index) > len(another_df.index)
            else concat([another_df, df], axis=1),
            results,
        )
        return result


def search_fields(
    data: Union[List[dict], dict], *fields: str
) -> DefaultDict[str, List[Any]]:
    """Search for fields.

    :param data: Data.
    :param fields: Fields for search
    :return: Dictionary with a list of found tags.
    """
    if not data:
        raise ValueError("Input data is empty.")
    if not fields:
        raise ValueError("Fields is empty.")

    found_fields = defaultdict(list)

    def __find_fields(piece_data: dict):
        for label, payload in piece_data.items():
            if label in fields:
                found_fields[label].append(payload)
            else:
                if isinstance(payload, dict):
                    __find_fields(payload)
                elif isinstance(payload, list):
                    for piece_payload in payload:
                        __find_fields(piece_payload)

    if isinstance(data, dict):
        data = [data]
    for piece in data:
        __find_fields(piece)

    return found_fields


def append_total_rows(
    data: DataFrameGroupBy, fields_options: Dict[str, str]
) -> Union[DataFrame, DataFrameGroupBy]:
    """Append total rows in data.

    :param data: Data.
    :param fields_options: Aggregate function for total rows.
    :return: DataFrame with total rows.
    """
    if fields_options:
        computes = []
        for field, option in fields_options.items():
            computes.append(
                data[field]
                .unstack()
                .assign(total=data[field].unstack().agg(option, axis=1))
                .stack()
                .to_frame(field)
            )
        return concat(computes, axis=1)
    else:
        return data


def delete_string_by_pattern(string: str, pattern: str) -> str:
    """Deletes string by pattern.

    :param string: String for delete.
    :param pattern: Pattern.
    :return: String with deleted pieces.
    """
    return sub(pattern, "", string)


def find_tag_in_string(data: str, search_tag: str) -> str:
    """Find tag value in record as string.

    :param data: Record as string.
    :param search_tag: Tag for search.
    :return: Tag value.
    """
    pattern = r"[\"']\S*[\"']"
    position = data.find(search_tag)
    if position != -1:
        position += len(search_tag)
        return search(pattern, data[position:]).group(0)[1:-1]


def aggregate_groups_by_intervals(
    data: Iterable[dict],
    time_field: str,
    *fields: str,
    intervals: str = "Q",
    total_row: bool = False,
    pivot: Union[Iterable[str], str] = None,
) -> DataFrame:
    """Aggregates by a field with specified interval.

    :param data: Data.
    :param time_field: Time field.
    :param fields: Fields for aggregate.
    :param intervals: Intervals.
    :param total_row: Adding a total row.
    :param pivot: Which columns must is pivoted.
    :return: Statistics.
    """
    if not data:
        raise ValueError("Input data is empty.")
    if not fields:
        raise ValueError("Fields is empty")

    df = DataFrame(data=data)

    time: Series = df.get(time_field)
    if time.empty:
        raise ValueError(f"{time_field} is empty.")
    elif time.dtype != "datetime64[ns]":
        raise ValueError(f"{time_field} isn't of type datetime64[ns]")

    df = (
        df.filter(items=[time_field, *fields])
        .set_index(time_field)
        .groupby([Grouper(freq=intervals), *fields], sort=True)
        .size()
        .reset_index(name="count")
        .set_index([time_field, *fields])
    )

    if pivot:
        if isinstance(pivot, str):
            pivot = (pivot,)
        index = [time_field] + [field for field in fields if field not in pivot]
        df = df.reset_index().pivot(index=index, columns=pivot, values="count")
    if total_row:
        index_length = len(df.index.names)
        name = ("Total",) * index_length if index_length > 1 else "Total"
        df.loc[name, :] = [
            column.sum() if str(column.dtype) != "object" else "Total"
            for _, column in df.items()
        ]
    return df


def create_tick_diagram(
    data: DataFrame, legend_to_table: bool = False
) -> Optional[DataFrame]:
    """Create ticks diagram.

    :param data: Data.
    :param legend_to_table: Whether to create legend in Dataframe.
    """
    fig = go.Figure()

    table = []
    if legend_to_table:
        for index, (element, payload) in enumerate(data.items()):
            fig.add_trace(
                go.Scatter(
                    name=index,
                    x=list(payload.keys()),
                    y=list(payload.values),
                    mode="lines",
                )
            )
            table.append({"index": index, "name": element})
    else:
        for element, payload in data.items():
            fig.add_trace(
                go.Scatter(
                    name="_".join(element) if not isinstance(element, str) else element,
                    x=list(payload.keys()),
                    y=list(payload.values),
                    mode="lines",
                )
            )

    fig.show()

    if legend_to_table:
        return DataFrame(table)
