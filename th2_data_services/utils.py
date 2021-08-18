from itertools import cycle, chain
from re import search, sub
from typing import Union, Dict, List, Optional
from IPython.display import display_html
from pandas import DataFrame, Grouper, concat
import plotly.graph_objects as go

FailedTags = List[Dict[str, Union[str, int]]]


class Utils:
    @staticmethod
    def aggregate_a_group(data: Union[dict, DataFrame], field: str) -> DataFrame:
        """Aggregate by a field.

        :param data: Data.
        :param field: Field for aggregation.
        :return: Statistics
        """
        if isinstance(data, DataFrame):
            if data.empty:
                raise ValueError("Input data is empty.")
        else:
            if not data:
                raise ValueError("Input data is empty.")

        df = DataFrame(data)

        if not df.get("status").any():
            raise ValueError("'status' is required field. Please add it.")

        df = (
            df.filter([field, "status"])
            .groupby([field, "status"])
            .size()
            .reset_index(name="count")
        )
        compute = DataFrame({field: df[field].unique()}).set_index(field)
        compute = (
            compute.join(
                df.groupby(field)
                .sum()
                .reset_index()
                .set_index(field)
                .rename(columns={"count": "total"}),
                on=field,
            )
            .join(
                df[df.status == "FAILED"]
                .groupby(field)
                .sum()
                .reset_index()
                .set_index(field)
                .rename(columns={"count": "fail"}),
                on=field,
            )
            .fillna(0)
        )
        compute.loc["Total"] = [compute["total"].sum(), compute["fail"].sum()]
        return compute

    @staticmethod
    def aggregate_groups(data: dict, *fields) -> DataFrame:
        """Aggregates by several fields.

        :param data: Data.
        :param fields: Fiealds for aggreagte.
        :return: Statistics.
        """
        if not data:
            raise ValueError("Input data is empty.")

        df = DataFrame(data)

        if not df.get("status").any():
            raise ValueError("'status' is required field. Please add it.")

        df = (
            df.filter([*fields, "status"])
            .groupby([*fields, "status"])
            .size()
            .reset_index(name="count")
        )
        compute = (
            DataFrame(data=df.groupby([*fields]).groups.keys())
            .rename(columns={index: field for index, field in enumerate(fields)})
            .set_index([*fields])
        )
        compute = (
            compute.join(
                df.groupby([*fields])
                .sum()
                .reset_index()
                .set_index([*fields])
                .rename(columns={"count": "total"}),
            )
            .join(
                df[df.status == "SUCCESSFUL"]
                .groupby([*fields])
                .sum()
                .reset_index()
                .set_index([*fields])
                .rename(columns={"count": "success"})
            )
            .join(
                df[df.status == "FAILED"]
                .groupby([*fields])
                .sum()
                .reset_index()
                .set_index([*fields])
                .rename(columns={"count": "fail"})
            )
            .fillna(0)
        )
        return compute

    @staticmethod
    def execute_aggregation(data: dict, filters: dict) -> dict:
        compute = {"all": 0}
        for entry in data:
            compute["all"] += 1
            for name, func in filters.items():
                if func(entry):
                    if compute.get(name):
                        compute[name] = 0
                    compute[name] += 1
        return compute

    @staticmethod
    def get_checked_tags(fields: dict, tags_set: set = None) -> set:
        if tags_set is None:
            tags_set = {"checked": set(), "presence_checked": set(), "ignored": set()}

        for tag, check in fields.items():
            type_ = check.get("type")
            if type_ == "field":
                if check.get("expected") == "null":
                    tags_set["ignored"].add(tag)
                elif check.get("operation") == "NOT_EMPTY":
                    tags_set["presence_checked"].add(tag)
                else:
                    tags_set["checked"].add(tag)
            elif type_ == "collection":
                Utils.get_checked_tags(check.get("fields"), tags_set)

        return tags_set

    @staticmethod
    def get_failed_tags(content: dict, tags: FailedTags = None) -> FailedTags:
        """Gets failed tags.

        :param content: Event content.
        :param tags: Failed tags.
        :return: Failed tags.
        """
        if tags is None:
            tags = []

        for field, payload in content.items():
            if isinstance(payload, dict):
                actual = payload.get("actual")
                expected = payload.get("expected")
                status = payload.get("status")
                operation = payload.get("operation")
                if actual and status == "FAILED":
                    tag = {
                        "failed_tag": field,
                        "failed_actual": actual,
                        f"failed_expected": expected,
                        f"failed_operation": operation,
                        "status": status,
                    }
                    if tag not in tags:
                        tags.append(tag)

                for value in payload.values():
                    if isinstance(value, dict):
                        Utils.get_failed_tags(payload, tags)

        return tags

    @staticmethod
    def find_tag(data: dict, search_tag: str) -> Optional[str]:
        """Finds first occurrence of a tag.

        :param data: Data.
        :param search_tag: Tag for search.
        :return: Tag value.
        """
        for field, payload in data.items():
            if field == search_tag:
                return payload

            if isinstance(payload, list):
                for info in payload:
                    if isinstance(info, dict):
                        tag = Utils.find_tag(info, search_tag)
                        if tag:
                            return tag
        return None

    @staticmethod
    def find_tag_everywhere(data: dict, search_tag: str, found_tags=None) -> List[str]:
        """Finds all occurrence of tag.

        :param data: Data.
        :param search_tag: Tag for search.
        :param found_tags: Found tags.
        :return: Found tags.
        """
        if found_tags is None:
            found_tags = []

        for field, payload in data.items():
            if field == search_tag:
                found_tags.append(payload)
                break

            if isinstance(payload, list):
                for info in payload:
                    if isinstance(info, dict):
                        Utils.find_tag_everywhere(info, search_tag, found_tags)
        return found_tags

    @staticmethod
    def find_tag_in_string(data: str, search_tag: str) -> str:
        """Find tag value in string.

        :param data: String.
        :param search_tag: Tag for search.
        :return: Tag value.
        """
        pattern = r"[\"']\S*[\"']"
        position = data.find(search_tag)
        if position != -1:
            position += len(search_tag)
            return search(pattern, data[position:]).group(0)[1:-1]

    @staticmethod
    def aggregate_a_group_by_intervals(
        data: dict, field: str, interval: str, **options: dict
    ) -> DataFrame:
        """Aggregates by a field with specified interval.

        :param data: Data.
        :param field: Field for aggregation.
        :param interval: Interval.
        :param options: Options.
        :return: Statistics.
        """
        if not data:
            raise ValueError("Input data is empty.")

        df = DataFrame(data=data)

        if not df.get("time").any():
            raise ValueError("'time' is required field. Please add it.")

        if options.get("status_off"):
            df = (
                df.filter(items=["time", field])
                .set_index("time")
                .sort_index()
                .groupby([Grouper(freq=interval), field])
                .size()
                .reset_index(name="count")
            )
        else:
            if not df.get("status").any():
                raise ValueError(
                    "'status' is required field. If you didn't need, you can use 'status_off=True'."
                )
            df = (
                df.filter(items=["time", "status", field])
                .set_index("time")
                .sort_index()
                .groupby([Grouper(freq=interval), field, "status"])
                .size()
                .reset_index(name="count")
            )

        filters = options.get("filter")

        compute = DataFrame(data={"time": df["time"].unique()}).merge(
            DataFrame(data={field: df[field].unique() if not filters else filters}),
            how="cross",
        )
        if options.get("status_off"):
            compute = compute.merge(df, on=["time", field], how="left")
            compute = compute.pivot(
                index=["time"], columns=[field], values="count"
            ).fillna(0)
        else:
            compute = compute.merge(
                DataFrame(data={"status": df["status"].unique()}), how="cross"
            ).merge(df, on=["time", field, "status"], how="left")
            compute = compute.pivot(
                index=["time"], columns=[field, "status"], values="count"
            ).fillna(0)

        return compute

    @staticmethod
    def create_tick_diagram(data: DataFrame, **options) -> Optional[DataFrame]:
        """Create ticks diagram.

        :param data: Data.
        :param options: options
        """
        fig = go.Figure()

        table = []
        if options.get("legend_to_table"):
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
                        name="_".join(element)
                        if not isinstance(element, str)
                        else element,
                        x=list(payload.keys()),
                        y=list(payload.values),
                        mode="lines",
                    )
                )

        fig.show()

        if options.get("legend_to_table"):
            return DataFrame(table)

    @staticmethod
    def aggregate_several_group(data: Union[DataFrame, dict], titles=cycle([""])):
        """Aggregates all groups in dataframe.

        :param data: Data.
        :param titles: Groups titles.
        :return: Show all groups in dataframe.
        """
        if not isinstance(data, DataFrame):
            data = DataFrame(data=data)

        if data.empty:
            raise ValueError("Input data is empty.")

        columns = list(data.columns)

        try:
            columns.index("status")
        except ValueError:
            raise ValueError("'status' is required field. Please add it.")

        columns.remove("status")

        results = []
        for column in columns:
            results.append(Utils.aggregate_a_group(data, column))

        html_str = ""
        for output, title in zip(results, chain(titles, cycle(["</br>"]))):
            html_str += '<th style="text-align: center"><td style="vertical-align:top">'
            html_str += f"<h2>{title}<h2>"
            html_str += output.to_html().replace(
                "table", 'table style="display:inline"'
            )
            html_str += "</td><th>"
        display_html(html_str, raw=True)

    @staticmethod
    def append_total_rows(data: DataFrame, fields_options: Dict[str, str]) -> DataFrame:
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

    @staticmethod
    def delete_string_by_pattern(string, pattern):
        """Deletes string by pattern.

        :param string: String for delete.
        :param pattern: Pattern.
        :return: String with deleted pieces.
        """
        return sub(pattern, "", string)

    @staticmethod
    def aggregate_a_group2(data: Union[dict, DataFrame], field: str) -> DataFrame:
        """Aggregate by a field.

        :param data: Data.
        :param field: Field for aggregation.
        :return: Statistics
        """
        if isinstance(data, DataFrame):
            if data.empty:
                raise ValueError("Input data is empty.")
        else:
            if not data:
                raise ValueError("Input data is empty.")

        df = DataFrame(data)

        if not df.get("status").any():
            raise ValueError("'status' is required field. Please add it.")

        df = (
            df.filter([field, "status"])
            .groupby([field, "status"])
            .size()
            .reset_index(name="count")
        )
        compute = DataFrame({field: df[field].unique()}).set_index(field)
        compute = compute.join(
            df.groupby(field)
            .sum()
            .reset_index()
            .set_index(field)
            .rename(columns={"count": "total"}),
            on=field,
        )
        compute.loc["Total"] = [compute["total"].sum()]
        return compute

    @staticmethod
    def aggregate_several_group2(data: Union[DataFrame, dict], titles=cycle([""])):
        """Aggregates all groups in dataframe.

        :param data: Data.
        :param titles: Groups titles.
        :return: Show all groups in dataframe.
        """
        if not isinstance(data, DataFrame):
            data = DataFrame(data=data)

        if data.empty:
            raise ValueError("Input data is empty.")

        columns = list(data.columns)

        try:
            columns.index("status")
        except ValueError:
            raise ValueError("'status' is required field. Please add it.")

        columns.remove("status")

        results = []
        for column in columns:
            results.append(Utils.aggregate_a_group2(data, column))

        html_str = ""
        for output, title in zip(results, chain(titles, cycle(["</br>"]))):
            html_str += '<th style="text-align: center"><td style="vertical-align:top">'
            html_str += f"<h2>{title}<h2>"
            html_str += output.to_html().replace(
                "table", 'table style="display:inline"'
            )
            html_str += "</td><th>"
        display_html(html_str, raw=True)
