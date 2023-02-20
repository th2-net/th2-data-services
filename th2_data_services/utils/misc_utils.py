from collections import defaultdict
from typing import List, Dict, Callable, Any, Tuple
from tabulate import tabulate
from datetime import datetime


# TODO - we have special converters for it in ds-2.0 (ProtobufTimestampConverter)
from th2_data_services.utils.time import timestamp_aggregation_key


class CategoryFrequencies(list):
    def __init__(self, val):
        """TODO - add.

        Args:
            val: add
        """
        super().__init__(val)

    def __repr__(self):
        return tabulate(self, headers="firstrow", tablefmt="grid")

    def _repr_html_(self):
        # TODO - non zero and non None values we can highlight
        # FOR Jupyter
        return tabulate(self, headers="firstrow", tablefmt="html")

    def __html__(self):
        self._repr_html_()

    def show_format(self, **kwargs):
        return tabulate(self, **kwargs)


# STREAMABLE
def get_objects_frequencies(
    objects_stream: List[Dict],
    categories: List,  # TODO - can be None to collect all values
    categorizer: Callable,
    timestamp_function: Callable,
    aggregation_level: str = "seconds",
    object_expander: Callable = None,
    objects_filter: Callable = None,
) -> CategoryFrequencies:
    """Returns objects frequencies based on categorizer.

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

    return CategoryFrequencies(results)


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
#   similar to totals for events, but evenets also have status field
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
