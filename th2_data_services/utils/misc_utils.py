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

from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, List, Tuple, Literal
from datetime import datetime, timezone

from deprecated.classic import deprecated

from th2_data_services.utils._types import Th2Event

# TODO - we have special converters for it in ds-2.0 (ProtobufTimestampConverter)
from th2_data_services.utils.aggregation_classes import CategoryFrequencies, FrequencyCategoryTable
from th2_data_services.utils.time import (
    timestamp_aggregation_key,
    _timestamp_rounded_down,
    _time_str_to_seconds,
    _round_timestamp_string_aggregation,
)


# TODO - we have get_objects_frequencies and get_objects_frequencies2 -- we need to unify it


@deprecated(reason='Use "get_objects_frequencies2" instead. It provides more advantages.')
def get_objects_frequencies(
    objects_stream: Iterable[Th2Event],
    categories: List,  # TODO - can be None to collect all values or []
    categorizer: Callable,
    timestamp_function: Callable,
    aggregation_level: str = "seconds",
    object_expander: Callable = None,
    objects_filter: Callable = None,
) -> CategoryFrequencies:
    """Returns objects frequencies based on categorizer.

    Returns timestamps in UTC format.

    Args:
        objects_stream: Objects stream
        categories: Categories list
        categorizer: Categorizer function
        timestamp_function: Timestamp function
        aggregation_level: Aggregation level
        object_expander: Object expander function
        objects_filter: Object filter function

    Returns:
        List[List]
    """
    frequencies = {}
    anchor = 0
    categories_set = set()
    for obj in objects_stream:
        expanded_objects = [obj] if object_expander is None else object_expander(obj)
        for expanded_object in expanded_objects:
            if objects_filter is not None:
                if not objects_filter(expanded_object):
                    continue

            if anchor == 0:
                anchor = timestamp_function(expanded_object)

            if not categories:
                epoch = timestamp_aggregation_key(
                    anchor, timestamp_function(expanded_object), aggregation_level
                )
                category = categorizer(expanded_object)
                categories_set.add(category)
                if epoch not in frequencies:
                    frequencies[epoch] = {category: 1}
                elif category not in frequencies[epoch]:
                    frequencies[epoch][category] = 1
                else:
                    frequencies[epoch][category] += 1
            else:
                for i in range(len(categories)):
                    if categorizer(expanded_object) == categories[i]:
                        epoch = timestamp_aggregation_key(
                            anchor, timestamp_function(expanded_object), aggregation_level
                        )
                        if epoch not in frequencies:
                            frequencies[epoch] = [0] * len(categories)
                        frequencies[epoch][i] += 1

    header = ["timestamp"]
    if categories:
        header.extend(categories)
    else:
        header.extend(categories_set)

    results = [header]
    timestamps = list(sorted(frequencies.keys()))
    for timestamp in timestamps:
        line = [datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")]
        if categories:
            line.extend(frequencies[timestamp])
        else:
            for category in categories_set:
                line.append(frequencies[timestamp][category]) if category in frequencies[
                    timestamp
                ] else line.append(0)

        results.append(line)

    return CategoryFrequencies(results)


# STREAMABLE
def get_objects_frequencies2(
    objects_stream: Iterable[Th2Event],
    categories: List[str],  # TODO - can be None to collect all values or []
    categorizer: Callable,
    timestamp_function: Callable,
    aggregation_level: str = "seconds",
    object_expander: Callable = None,
    objects_filter: Callable = None,
    gap_mode: Literal[1, 2, 3] = 1,
    zero_anchor: bool = False,
    include_total: bool = True,
) -> FrequencyCategoryTable:
    # TODO - used by both messages and events get_category_frequencies
    """Returns objects frequencies based on categorizer.

    Returns timestamps in UTC format.

    For more info please see: https://github.com/th2-net/th2-data-services/blob/dev_2.0.0/documentation/frequencies.md

    Args:
        objects_stream: Objects stream
        categories: Categories list.
            Provide [] or None to collect all possible values.
        categorizer: Categorizer function
        timestamp_function: Timestamp function
        aggregation_level: Aggregation level
        object_expander: Object expander function
        objects_filter: Object filter function
        gap_mode:
            1 - Every range starts with actual message timestamp,
            2 - Ranges are split equally,
            3 - Same as 2, but filled with empty ranges in between
        zero_anchor: If False anchor used is first timestamp from message, if True anchor is 0
        include_total: Will add Total column if True.

    Returns:
        List[List]

    Examples:
        It'll return the table like this.
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | timestamp_start   | timestamp_end   | ExecutionReport   | NewOrder   | OrderCancel   |   Total |
        +========+===================+=================+===================+============+===============+=========+
        |        | 2023-08-13        | 2023-08-14      | 1                 | 1          | 2             |       4 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-14        | 2023-08-15      | 1                 | 1          | 2             |       4 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-16        | 2023-08-17      | 0                 | 2          | 3             |       5 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-17        | 2023-08-18      | 1                 | 0          | 1             |       2 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-19        | 2023-08-20      | 1                 | 1          | 0             |       2 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-20        | 2023-08-21      | 0                 | 0          | 2             |       2 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-21        | 2023-08-22      | 1                 | 3          | 0             |       4 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-22        | 2023-08-23      | 1                 | 0          | 0             |       1 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-23        | 2023-08-24      | 0                 | 3          | 0             |       3 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        |        | 2023-08-24        | 2023-08-25      | 0                 | 2          | 1             |       3 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        | count  |                   |                 |                   |            |               |      10 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
        | totals |                   |                 | 6                 | 13         | 11            |      30 |
        +--------+-------------------+-----------------+-------------------+------------+---------------+---------+
    """
    if gap_mode == 1 and zero_anchor:
        raise Exception("gap_mode=1 and zero_anchor=True are not supported together")
    TOTAL_FIELD = "Total"
    frequencies = {}
    anchor = 0
    categories_set = set()
    object_list = []
    for obj in objects_stream:
        object_list += [obj] if object_expander is None else object_expander(obj)

    object_list = sorted(object_list, key=timestamp_function)

    for obj in object_list:
        if objects_filter is not None:
            if not objects_filter(obj):
                continue

        if not zero_anchor:
            if anchor == 0:
                anchor = _timestamp_rounded_down(timestamp_function(obj), aggregation_level)
            if (
                gap_mode == 1
                and timestamp_aggregation_key(anchor, timestamp_function(obj), aggregation_level)
                != anchor
            ):
                anchor = _timestamp_rounded_down(timestamp_function(obj), aggregation_level)
        if not categories:
            epoch = timestamp_aggregation_key(anchor, timestamp_function(obj), aggregation_level)
            if include_total:
                if epoch not in frequencies:
                    frequencies[epoch] = {TOTAL_FIELD: 0}
                if TOTAL_FIELD not in frequencies[epoch]:
                    frequencies[epoch][TOTAL_FIELD] = 1
                else:
                    frequencies[epoch][TOTAL_FIELD] += 1
            category = categorizer(obj)
            categories_set.add(category)
            if epoch not in frequencies:
                frequencies[epoch] = {category: 0}
            if category not in frequencies[epoch]:
                frequencies[epoch][category] = 1
            else:
                frequencies[epoch][category] += 1
        else:
            for category in categories:
                if categorizer(obj) == category:
                    epoch = timestamp_aggregation_key(
                        anchor, timestamp_function(obj), aggregation_level
                    )
                    if epoch not in frequencies:
                        frequencies[epoch] = {category: 0}
                    if category not in frequencies[epoch]:
                        frequencies[epoch][category] = 0
                    frequencies[epoch][category] += 1
                    if include_total:
                        if TOTAL_FIELD not in frequencies[epoch]:
                            frequencies[epoch][TOTAL_FIELD] = 0
                        frequencies[epoch][TOTAL_FIELD] += 1

    sorted_categories = sorted(categories_set)

    header = ["timestamp_start", "timestamp_end"]
    if categories:
        header.extend(categories)
    else:
        header.extend(sorted_categories)

    if include_total:
        header.append(TOTAL_FIELD)

    results = [header]
    timestamps = list(sorted(frequencies.keys()))
    # Expected that timestamp is seconds.
    if gap_mode == 3:
        last_timestamp = timestamps[0]
        timestamps_with_zeros = [timestamps[0]]
        for timestamp in timestamps[1:]:
            for zero_timestamp in range(
                last_timestamp + _time_str_to_seconds(aggregation_level),
                timestamp,
                _time_str_to_seconds(aggregation_level),
            ):
                timestamps_with_zeros.append(zero_timestamp)
                frequencies[zero_timestamp] = []
            timestamps_with_zeros.append(timestamp)
            last_timestamp = timestamp
        timestamps = timestamps_with_zeros

    for timestamp in timestamps:
        st_string = _round_timestamp_string_aggregation(timestamp, aggregation_level)
        et_string = _round_timestamp_string_aggregation(
            timestamp + _time_str_to_seconds(aggregation_level), aggregation_level
        )
        line = [st_string, et_string]
        if categories:
            line.extend(frequencies[timestamp].values())
        else:
            for category in sorted_categories:
                line.append(frequencies[timestamp][category]) if category in frequencies[
                    timestamp
                ] else line.append(0)
            if include_total:
                line.append(sum(line[2:]))

        results.append(line)

    r = FrequencyCategoryTable(header=header, rows=results[1:])

    return r


# STREAMABLE (?)
def analyze_stream_sequence(
    stream: Iterable[Th2Event],
    sequence_extractor: Callable,
    timestamp_extractor: Callable,
    seq_filter: Callable = None,
    object_expander: Callable = None,
) -> List[Dict]:
    """Analyzes stream sequence.

    Args:
        stream: Sequence of objects
        sequence_extractor: Sequence extractor function
        timestamp_extractor: Timestamp extractor function
        seq_filter: Sequence filter function
        object_expander: Object expander function

    Returns:
        List[Dict]
    """
    stream_list = []  # SortedKeyList(key=lambda t: t[0])
    zero_indexes = 0
    for obj in stream:
        expanded_objects = [obj] if object_expander is None else object_expander(obj)
        for expanded_object in expanded_objects:
            if seq_filter is not None and not seq_filter(expanded_object):
                continue
            seq = sequence_extractor(expanded_object)
            if seq == 0:
                zero_indexes += 1
                continue

            stream_list.append((seq, timestamp_extractor(expanded_object)))

    result = []
    if len(stream_list) == 0:
        result.append({"type": "summary", "is_empty": True})
        return result

    if zero_indexes > 0:
        result.append({"type": "summary", "zero_sequence_numbers": zero_indexes})

    print(f"Got stream len = {len(stream_list)}")

    # split into intervals between
    stream_list.sort(key=lambda t: t[1])
    prev_start = 0
    chunks = []
    for i in range(1, len(stream_list)):
        if stream_list[i][0] < stream_list[i - 1][0]:
            chunks.append(stream_list[prev_start:i])  # New chunk
            prev_start = i

    chunks.append(stream_list[prev_start:])  # New chunk
    print(f"Got {len(chunks)} chunks")

    # check gaps in each interval
    for chunk in chunks:
        chunk.sort(key=lambda t: t[0])
        result.append(
            {
                "type": "chunk_summary",
                "seq_1": chunk[0][0],
                "seq_2": chunk[len(chunk) - 1][0],
                "timestamp_1": chunk[0][1],
                "timestamp_2": chunk[len(chunk) - 1][1],
            }
        )

        prev_seq = -1
        prev_time = None
        for entry in chunk:
            curr_seq = entry[0]
            curr_time = entry[1]
            if prev_seq != -1:
                if curr_seq - prev_seq > 1:
                    result.append(
                        {
                            "type": "gap",
                            "seq_1": prev_seq,
                            "seq_2": curr_seq,
                            "timestamp_1": prev_time,
                            "timestamp_2": curr_time,
                        }
                    )
                if curr_seq == prev_seq:
                    result.append(
                        {
                            "type": "duplicate",
                            "seq": prev_seq,
                            "timestamp_1": prev_time,
                            "timestamp_2": curr_time,
                        }
                    )
            prev_seq = curr_seq
            prev_time = curr_time

    return result


# STREAMABLE ?
def process_objects_stream(
    stream: Iterable[Th2Event], processors: List[Tuple[Callable, Dict]], expander: Callable = None
) -> None:
    """Processes object stream with processors.

    Args:
        stream: Object stream
        processors: Processor function: params
        expander: Object expander function

    """
    for obj in stream:
        if expander is None:
            for processor, params in processors:
                processor(obj, **params)
        else:
            expaned_objects = expander(obj)
            for expaned_object in expaned_objects:
                for processor, params in processors:
                    processor(expaned_object, **params)


# TODO: Is this useful?
#   similar to totals for events, but evenets also have status field
def get_category_totals_p(
    obj: Dict, categorizer: Callable, obj_filter: Callable, result
) -> Any:  # noqa
    # TODO: Add docstings
    if obj is None:
        return get_category_totals_p, {
            "categorizer": categorizer,
            "obj_filter": obj_filter,
            "result": result,
        }

    if obj_filter is not None and not obj_filter(obj):
        return None

    category = categorizer(obj)
    if category not in result:
        result[category] = 1
    else:
        result[category] = result[category] + 1

    return None


def get_category_examples_p(
    obj: Dict,
    categorizer: Callable,
    obj_filter: Callable,
    cat_filter: Callable,
    max_qty: int,
    result,
) -> Any:  # noqa
    if obj is None:
        return get_category_examples_p, {
            "categorizer": categorizer,
            "obj_filter": obj_filter,
            "cat_filter": cat_filter,
            "max_qty": max_qty,
            "result": result,
        }
    if obj_filter is not None and not obj_filter(obj):
        return None

    category = categorizer(obj)
    if cat_filter is not None and not cat_filter(category):
        return None

    if category not in result:
        result[category] = [obj]
        return None
    if len(result[category]) < max_qty:
        result[category].append(obj)


# TODO: Is this useful?
#   Used by get_category_measurement_p
def update_int_measurement(metric: int, measurement_data):  # noqa
    # TODO: Add docstings
    count = 1
    if "count" in measurement_data:
        count = measurement_data["count"]

    m_avg = float(metric)
    m_max = metric
    m_min = metric
    if count > 1:
        m_prev_avg = measurement_data["avg"]
        m_avg = m_prev_avg * count / (count + 1) + float(metric) / (count + 1)
        m_max = measurement_data["max"]
        m_min = measurement_data["min"]
        if metric > m_max:
            m_max = metric
        if metric < m_min:
            m_min = metric

    measurement_data["count"] = count + 1
    measurement_data["avg"] = m_avg
    measurement_data["min"] = m_min
    measurement_data["max"] = m_max

    if "distr" not in measurement_data:
        measurement_data["distr"] = {metric: 1}
    else:
        if metric not in measurement_data["distr"]:
            measurement_data["distr"][metric] = 1
        else:
            measurement_data["distr"][metric] += 1


# TODO: Is this useful?
def get_category_measurement_p(obj, categorizer, measurement_func, obj_filter, result):  # noqa
    # TODO: Add docstrings

    if obj is None:
        return get_category_measurement_p, {
            "categorizer": categorizer,
            "measurement_func": measurement_func,
            "obj_filter": obj_filter,
            "result": result,
        }

    if obj_filter is not None and not obj_filter(obj):
        return None

    category = categorizer(obj)
    value = measurement_func(obj)
    data_point = {}
    if category not in result:
        result[category] = data_point
    else:
        data_point = result[category]

    update_int_measurement(value, data_point)
    return None


# STREAMABLE
def create_qty_distribution(categories: Dict, category_filter: Callable) -> Dict:
    """Returns qty distribution.

    Args:
        categories: Categories dictionary
        category_filter: Category filter

    Returns:
        Dict
    """
    result = defaultdict(int)
    for key, value in categories.items():
        if category_filter(key):
            result[value] += 1

    return result


def calc_percentile_in_measurement_dict(d):  # noqa
    # TODO - something strange ..
    #   nothing uses it.
    #   it doesn't return anything
    for item in d.values():
        distr = item["distr"]
        total = item["count"]
        x_series = list(distr.keys())
        x_series.sort()
        sum = 0
        x_prev = 0
        for x in x_series:
            sum += distr[x]
            if sum > 0.5 * total:
                if "max50" not in item:
                    item["max50"] = x_prev
            if sum > 0.9 * total:
                if "max90" not in item:
                    item["max90"] = x_prev
            if sum > 0.99 * total:
                if "max99" not in item:
                    item["max99"] = x_prev
            if sum > 0.999 * total:
                if "max99.9" not in item:
                    item["max99.9"] = x_prev
            x_prev = x

        if "max50" not in item:
            item["max50"] = x_prev
        if "max90" not in item:
            item["max90"] = x_prev
        if "max99" not in item:
            item["max99"] = x_prev
        if "max99.9" not in item:
            item["max99.9"] = x_prev
