<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/time.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.time`





---

<a href="../../th2_data_services/utils/time.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/time.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/time.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/time.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `time_slice_object_filter`

```python
time_slice_object_filter(
    timestamp_field: Dict,
    timestamp_iso: str,
    duration_seconds: int
)
```






---

<a href="../../th2_data_services/utils/time.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `timestamp_aggregation_key`

```python
timestamp_aggregation_key(
    global_anchor_timestamp: int,
    timestamp: int,
    aggregation_level: str = 'seconds'
) → int
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
