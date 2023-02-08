from tabulate import tabulate
from datetime import datetime


def print_stats_dict(d, return_html=False, sort_values=False, tabulate_style="grid"):
    table = [["category", "count"]]
    total = 0
    data = []
    for item in d.items():
        data.append([item[0], str(item[1])])
        total = total + item[1]
    if sort_values:
        data.sort(key=lambda m: int(m[1]), reverse=True)

    table.extend(data)
    table.append(["CATEGORIES", str(len(d))])
    table.append(["TOTAL", str(total)])

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt=tabulate_style))
        return None


def print_measurement_dict(d, return_html=False):
    header_set = set()
    for item in d.values():
        for k in item.keys():
            if k == "distr":
                continue
            header_set.add(k)

    header = list(header_set)
    header.sort()
    table = [["category"]]
    table[0].extend(header)

    for k, v in d.items():
        row = [k]
        for s in header:
            row.append(str(v[s]))
        table.append(row)

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
        return None


def extract_time_string(timestamp_element):
    t = datetime.fromtimestamp(timestamp_element["epochSecond"])
    return t.isoformat() + "." + str(timestamp_element["nano"]).zfill(9)


def time_interval_filter_seconds_precision(timestamp_element, start_timestamp, end_timestamp):
    return start_timestamp <= timestamp_element["epochSecond"] <= end_timestamp


def timestamp_delta_us(start, end):
    return (end["epochSecond"] - start["epochSecond"]) * 1000000 + (end["nano"] - start["nano"])/1000


def timestamp_aggregation_key(global_anchor_timestamp, timestamp, aggregation_level="seconds"):
    if aggregation_level == "seconds":
        return timestamp

    interval = 1

    if aggregation_level == "minutes":
        interval = 60
    elif aggregation_level == "hours":
        interval = 3600
    elif aggregation_level == "30min":
        interval = 1800
    elif aggregation_level == "5min":
        interval = 300
    elif aggregation_level == "1min":
        interval = 60
    elif aggregation_level == "10sec":
        interval = 10
    elif aggregation_level == "30sec":
        interval = 30

    return global_anchor_timestamp+interval*((timestamp-global_anchor_timestamp)//interval)


def get_objects_frequencies(objects_stream, categories_list, categorizer_function, timestamp_function,
                            aggregation_level="seconds", object_expander=None, objects_filter=None):
    freq = {}
    anchor = 0
    my_cat_set = set()
    for obj in objects_stream:
        oo = []
        if object_expander is None:
            oo = [obj]
        else:
            oo = object_expander(obj)
        for o in oo:
            if objects_filter is not None:
                if not objects_filter(o):
                    continue

            if anchor == 0:
                anchor = timestamp_function(o)

            if categories_list is None or len(categories_list) == 0:
                epoch = timestamp_aggregation_key(anchor, timestamp_function(o), aggregation_level)
                category = categorizer_function(o)
                my_cat_set.add(category)
                if epoch not in freq:
                    freq[epoch] = {category: 1}
                elif category not in freq[epoch]:
                    freq[epoch][category] = 1
                else:
                    freq[epoch][category] = freq[epoch][category] + 1

            else:
                for i in range(len(categories_list)):
                    if categorizer_function(o) == categories_list[i]:
                        epoch = timestamp_aggregation_key(anchor, timestamp_function(o), aggregation_level)
                        if epoch not in freq:
                            freq[epoch] = [0] * len(categories_list)
                        freq[epoch][i] = freq[epoch][i] + 1

    header = ["timestamp"]
    if categories_list is None or len(categories_list) == 0:
        header.extend(my_cat_set)
    else:
        header.extend(categories_list)

    ft = [header]

    timestamps = list(freq.keys())
    timestamps.sort()

    for t in timestamps:
        line = [datetime.fromtimestamp(t).isoformat()]
        if categories_list is None or len(categories_list) == 0:
            for c in my_cat_set:
                line.append(freq[t][c]) if c in freq[t] else line.append(0)
        else:
            line.extend(freq[t])
        ft.append(line)

    return ft


def analyze_stream_sequence(stream, sequence_extractor, timestamp_extractor, seq_filter=None,object_expander=None):
    stream_list = [] #SortedKeyList(key=lambda t: t[0])
    zero_indexes = 0
    for obj in stream:
        oo = []
        if object_expander is None:
            oo = [obj]
        else:
            oo = object_expander(obj)
        for o in oo:
            if seq_filter is not None and not seq_filter(o):
                continue
            seq = sequence_extractor(o)
            if seq == 0:
                zero_indexes = zero_indexes + 1
                continue

            stream_list.append((sequence_extractor(o), timestamp_extractor(o)))

    result = []
    if len(stream_list) == 0:
        result.append({"type": "summary",
                      "is_empty": True})
        return result

    if zero_indexes > 0:
        result.append({"type": "summary",
                      "zero_sequence_numbers": zero_indexes})

    print("Got stream len = ",len(stream_list))

    #split into intervals between
    stream_list.sort(key=lambda t: t[1])
    prev_start = 0
    chunks = []
    for i in range(1, len(stream_list)):
        if stream_list[i][0] < stream_list[i-1][0]:
            #new chunk
            chunk = []
            chunk.extend(stream_list[prev_start:i])
            chunks.append(chunk)
            prev_start = i

    chunk = []
    chunk.extend(stream_list[prev_start:])
    chunks.append(chunk)
    print("Got ", len(chunks), " chunks")

    #check gaps in each interval

    for chunk in chunks:
        chunk.sort(key=lambda t: t[0])
        result.append({"type": "chunk_summary",
                       "seq_1": chunk[0][0],
                       "seq_2": chunk[len(chunk) - 1][0],
                       "timestamp_1": chunk[0][1],
                       "timestamp_2": chunk[len(chunk) - 1][1]})

        prev_seq = -1
        prev_time = None
        for entry in chunk:
            curr_seq = entry[0]
            curr_time = entry[1]
            if prev_seq != -1:
                if curr_seq - prev_seq > 1:
                    result.append({"type": "gap",
                                   "seq_1": prev_seq,
                                   "seq_2": curr_seq,
                                   "timestamp_1": prev_time,
                                   "timestamp_2": curr_time})
                if curr_seq == prev_seq:
                    result.append({"type": "duplicate",
                                   "seq": prev_seq,
                                   "timestamp_1": prev_time,
                                   "timestamp_2": curr_time})
            prev_seq = curr_seq
            prev_time = curr_time

    return result


def time_slice_object_filter(timestamp_field, str_time, duration_seconds):
    #trying to commit
    ts1 = datetime.fromisoformat(str_time).timestamp()
    ts2 = ts1 + duration_seconds

    return lambda o: time_interval_filter_seconds_precision(o[timestamp_field], ts1, ts2)


def process_objects_stream(stream, processors, expander=None):

    for obj in stream:
        if expander is None:
            for func, params in processors:
                func(obj, **params)
        else:
            oo = expander(obj)
            for o in oo:
                for func, params in processors:
                    func(o, **params)


def get_category_totals_p(obj, categorizer, obj_filter, result):
    if obj is None:
        return get_category_totals_p, {"categorizer": categorizer, "obj_filter": obj_filter, "result": result}

    if obj_filter is not None and not obj_filter(obj):
        return None

    category = categorizer(obj)
    if category not in result:
        result[category] = 1
    else:
        result[category] = result[category] + 1

    return None


def update_int_measurement(metric : int, measurement_data, exp_10_bucket : int = 0):
    count = 1
    if "count" in measurement_data:
        count = measurement_data["count"]

    m_avg = float(metric)
    m_max = metric
    m_min = metric
    if count > 1:
        m_prev_avg = measurement_data["avg"]
        m_avg = m_prev_avg*count/(count+1)+float(metric)/(count+1)
        m_max = measurement_data["max"]
        m_min = measurement_data["min"]
        if metric >  m_max:
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


def get_category_measurement_p(obj, categorizer, measurement_func, obj_filter, result):
    if obj is None:
        return get_category_measurement_p, {"categorizer": categorizer, "measurement_func": measurement_func, "obj_filter": obj_filter, "result": result}

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


def create_qty_distribution(category_dict, category_filter):
    result = {}
    for k,v in category_dict.items():
        if category_filter(k):
            qty = v
            if v not in result:
                result[v] = 1
            else:
                result[v] += 1
    return result
