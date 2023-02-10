from collections import defaultdict
from typing import List, Dict, Union, Callable, Any, Tuple
from tabulate import tabulate
from datetime import datetime


# STREAMABLE
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

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt=tabulate_style))
        return None


# STREAMABLE
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


# STREAMABLE
def extract_timestamp(timestamp_element: Dict) -> str:
    """Extracts timestamp from argument.

    Args:
        timestamp_element:

    Returns:
        str
    """
    timestamp = datetime.fromtimestamp(timestamp_element["epochSecond"])
    return f"{timestamp.isoformat()}.{timestamp_element['nano'].zfill(9)}"


# STREAMABLE
def time_interval_filter_seconds_precision(
    timestamp_element: Dict, start_timestamp: Union[int, float], end_timestamp: Union[int, float]
) -> bool:
    """TODO: Add Description.

    Args:
        timestamp_element: Timestamp element
        start_timestamp: Start timestamp
        end_timestamp: End timestamp

    Returns:
        bool
    """
    return start_timestamp <= timestamp_element["epochSecond"] <= end_timestamp


# STREAMABLE
def timestamp_delta_us(start_timestamp: Dict, end_timestamp: Dict) -> float:
    """Returns timestamp delta in milliseconds.

    Args:
        start_timestamp: Start timestamp
        end_timestamp: End timestamp

    Returns:
        float
    """
    seconds_delta = (end_timestamp["epochSecond"] - start_timestamp["epochSecond"]) * 1000000
    nano_delta = (end_timestamp["nano"] - start_timestamp["nano"]) / 1000
    return seconds_delta + nano_delta


def timestamp_aggregation_key(
    global_anchor_timestamp: int, timestamp: int, aggregation_level: str = "seconds"
) -> int:  # noqa
    # TODO: Add docstings
    if aggregation_level == "seconds":
        return timestamp

    aggregation_levels = {
        "minutes": 60,
        "30min": 1800,
        "hours": 3600,
        "1min": 60,
        "5min": 300,
        "10sec": 10,
        "30sec": 30,
    }
    try:
        interval = aggregation_levels[aggregation_level]
    except KeyError:
        raise KeyError(f"Invalid aggregation level. Available levels: {', '.join(aggregation_levels)}")

    return global_anchor_timestamp + interval * ((timestamp - global_anchor_timestamp) // interval)


# STREAMABLE
def get_objects_frequencies(
    objects_stream: List[Dict],
    categories: List,
    categorizer: Callable,
    timestamp_function: Callable,
    aggregation_level: str = "seconds",
    object_expander: Callable = None,
    objects_filter: Callable = None,
) -> List[List]:
    """Gets objects frequencies.

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
                epoch = timestamp_aggregation_key(anchor, timestamp_function(expanded_object), aggregation_level)
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
        line = [datetime.fromtimestamp(timestamp).isoformat()]
        if categories:
            line.extend(frequencies[timestamp])
        else:
            for category in categories_set:
                line.append(frequencies[timestamp][category]) if category in frequencies[timestamp] else line.append(0)

        results.append(line)

    return results


# STREAMABLE (?)
def analyze_stream_sequence(
    stream: List[Dict],
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
                        {"type": "duplicate", "seq": prev_seq, "timestamp_1": prev_time, "timestamp_2": curr_time}
                    )
            prev_seq = curr_seq
            prev_time = curr_time

    return result


# STREAMABLE
def time_slice_object_filter(timestamp_field: Dict, timestamp_iso: str, duration_seconds: int):  # noqa
    # TODO: Add docstings
    ts1 = datetime.fromisoformat(timestamp_iso).timestamp()
    ts2 = ts1 + duration_seconds

    return lambda obj: time_interval_filter_seconds_precision(obj[timestamp_field], ts1, ts2)


# STREAMABLE ?
def process_objects_stream(
    stream: List[Dict], processors: List[Tuple[Callable, Dict]], expander: Callable = None
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
def get_category_totals_p(record: Dict, categorizer: Callable, filter_: Callable, result) -> Any:  # noqa
    # TODO: Add docstings
    if record is None:
        return get_category_totals_p, {"categorizer": categorizer, "obj_filter": filter_, "result": result}

    if filter_ is not None and not filter_(record):
        return None

    category = categorizer(record)
    if category not in result:
        result[category] = 1
    else:
        result[category] += 1


# TODO: Is this useful?
# TODO: Is `exp_10_bucket` argument necessary?
def update_int_measurement(metric: int, measurement_data, exp_10_bucket: int = 0):  # noqa
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
