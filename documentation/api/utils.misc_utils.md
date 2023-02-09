<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/misc_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.misc_utils`





---

<a href="../../th2_data_services/utils/misc_utils.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_stats_dict`

```python
print_stats_dict(d, return_html=False, sort_values=False, tabulate_style='grid')
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_measurement_dict`

```python
print_measurement_dict(d, return_html=False)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_time_string`

```python
extract_time_string(timestamp_element)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `time_interval_filter_seconds_precision`

```python
time_interval_filter_seconds_precision(
    timestamp_element,
    start_timestamp,
    end_timestamp
)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `timestamp_delta_us`

```python
timestamp_delta_us(start, end)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `timestamp_aggregation_key`

```python
timestamp_aggregation_key(
    global_anchor_timestamp,
    timestamp,
    aggregation_level='seconds'
)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_objects_frequencies`

```python
get_objects_frequencies(
    objects_stream,
    categories_list,
    categorizer_function,
    timestamp_function,
    aggregation_level='seconds',
    object_expander=None,
    objects_filter=None
)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `analyze_stream_sequence`

```python
analyze_stream_sequence(
    stream,
    sequence_extractor,
    timestamp_extractor,
    seq_filter=None,
    object_expander=None
)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `time_slice_object_filter`

```python
time_slice_object_filter(timestamp_field, str_time, duration_seconds)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_objects_stream`

```python
process_objects_stream(stream, processors, expander=None)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_category_totals_p`

```python
get_category_totals_p(obj, categorizer, obj_filter, result)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_int_measurement`

```python
update_int_measurement(metric: int, measurement_data, exp_10_bucket: int = 0)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L300"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_category_measurement_p`

```python
get_category_measurement_p(
    obj,
    categorizer,
    measurement_func,
    obj_filter,
    result
)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_qty_distribution`

```python
create_qty_distribution(category_dict, category_filter)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
