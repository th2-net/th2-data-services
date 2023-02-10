<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/misc_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.misc_utils`





---

<a href="../../th2_data_services/utils/misc_utils.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_stats_dict`

```python
print_stats_dict(
    data: Dict,
    return_html: bool = False,
    sort_values: bool = False,
    tabulate_style: str = 'grid'
) → Union[NoneType, str]
```

Prints Statistics. 



**Args:**
 
 - <b>`data`</b>:  Dictionary of data 
 - <b>`return_html`</b>:  Return HTML format, defaults to False 
 - <b>`sort_values`</b>:  Sort result, defaults to False 
 - <b>`tabulate_style`</b>:  Table format style, defaults to "grid" 



**Returns:**
 None if return_html is False else str 


---

<a href="../../th2_data_services/utils/misc_utils.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_measurement_dict`

```python
print_measurement_dict(data: Dict, return_html: bool = False)
```

Prints Measurements. 



**Args:**
 
 - <b>`data`</b>:  Dictionary of data 
 - <b>`return_html`</b>:  Return HTML format, defaults to False 



**Returns:**
 None if return_html is False else str 


---

<a href="../../th2_data_services/utils/misc_utils.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_timestamp`

```python
extract_timestamp(timestamp_element: Dict) → str
```

Extracts timestamp from argument. 



**Args:**
  timestamp_element: 



**Returns:**
  str 


---

<a href="../../th2_data_services/utils/misc_utils.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `time_interval_filter_seconds_precision`

```python
time_interval_filter_seconds_precision(
    timestamp_element: Dict,
    start_timestamp: Union[int, float],
    end_timestamp: Union[int, float]
) → bool
```

TODO: Add Description. 



**Args:**
 
 - <b>`timestamp_element`</b>:  Timestamp element 
 - <b>`start_timestamp`</b>:  Start timestamp 
 - <b>`end_timestamp`</b>:  End timestamp 



**Returns:**
 bool 


---

<a href="../../th2_data_services/utils/misc_utils.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `timestamp_delta_us`

```python
timestamp_delta_us(start_timestamp: Dict, end_timestamp: Dict) → float
```

Returns timestamp delta in milliseconds. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp 
 - <b>`end_timestamp`</b>:  End timestamp 



**Returns:**
 float 


---

<a href="../../th2_data_services/utils/misc_utils.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `timestamp_aggregation_key`

```python
timestamp_aggregation_key(
    global_anchor_timestamp: int,
    timestamp: int,
    aggregation_level: str = 'seconds'
) → int
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_objects_frequencies`

```python
get_objects_frequencies(
    objects_stream: List[Dict],
    categories: List,
    categorizer: Callable,
    timestamp_function: Callable,
    aggregation_level: str = 'seconds',
    object_expander: Callable = None,
    objects_filter: Callable = None
) → List[List]
```

Gets objects frequencies. 



**Args:**
 
 - <b>`objects_stream`</b>:  Objects stream 
 - <b>`categories`</b>:  Categories list 
 - <b>`categorizer`</b>:  Categorizer function 
 - <b>`timestamp_function`</b>:  Timestamp function 
 - <b>`aggregation_level`</b>:  Aggregation level 
 - <b>`object_expander`</b>:  Object expander function 
 - <b>`objects_filter`</b>:  Object filter function 



**Returns:**
 List[List] 


---

<a href="../../th2_data_services/utils/misc_utils.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `analyze_stream_sequence`

```python
analyze_stream_sequence(
    stream: List[Dict],
    sequence_extractor: Callable,
    timestamp_extractor: Callable,
    seq_filter: Callable = None,
    object_expander: Callable = None
) → List[Dict]
```

Analyzes stream sequence. 



**Args:**
 
 - <b>`stream`</b>:  Sequence of objects 
 - <b>`sequence_extractor`</b>:  Sequence extractor function 
 - <b>`timestamp_extractor`</b>:  Timestamp extractor function 
 - <b>`seq_filter`</b>:  Sequence filter function 
 - <b>`object_expander`</b>:  Object expander function 



**Returns:**
 List[Dict] 


---

<a href="../../th2_data_services/utils/misc_utils.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `time_slice_object_filter`

```python
time_slice_object_filter(
    timestamp_field: Dict,
    timestamp_iso: str,
    duration_seconds: int
)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L325"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_objects_stream`

```python
process_objects_stream(
    stream: List[Dict],
    processors: List[Tuple[Callable, Dict]],
    expander: Callable = None
) → None
```

Processes object stream with processors. 



**Args:**
 
 - <b>`stream`</b>:  Object stream 
 - <b>`processors`</b>:  Processor function: params 
 - <b>`expander`</b>:  Object expander function 


---

<a href="../../th2_data_services/utils/misc_utils.py#L348"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_category_totals_p`

```python
get_category_totals_p(
    record: Dict,
    categorizer: Callable,
    filter_: Callable,
    result
) → Any
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_int_measurement`

```python
update_int_measurement(metric: int, measurement_data, exp_10_bucket: int = 0)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L399"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/misc_utils.py#L426"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_qty_distribution`

```python
create_qty_distribution(categories: Dict, category_filter: Callable) → Dict
```

Returns qty distribution. 



**Args:**
 
 - <b>`categories`</b>:  Categories dictionary 
 - <b>`category_filter`</b>:  Category filter 



**Returns:**
 Dict 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
