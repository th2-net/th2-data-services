<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/utils/converter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.utils.converter`






---

<a href="../../th2_data_services/interfaces/utils/converter.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ITimestampConverter`







---

<a href="../../th2_data_services/interfaces/utils/converter.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(timestamp: ~TimestampType) → Tuple[str, str]
```

Returns string representation of Unix time. 

Separated for seconds and nanoseconds. 

Please note, nanoseconds can have zeroes from left. 

e.g. 2022-03-05T23:56:44.00123Z -> ('1646524604', '001230000') 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp_int`

```python
parse_timestamp_int(timestamp: ~TimestampType) → Tuple[int, int]
```

Returns int representation of Unix time. 

Separated for seconds and nanoseconds. 

e.g. 2022-03-05T23:56:44.00123Z -> (1646524604, 001230000) 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_datetime`

```python
to_datetime(timestamp: ~TimestampType) → datetime
```

Converts timestamp to UTC datetime object. 

If your timestamp has nanoseconds, they will be just cut (not rounded). 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`datetime`</b>:  Timestamp in python datetime format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_datetime_str`

```python
to_datetime_str(timestamp: ~TimestampType) → str
```

Converts timestamp to UTC datetime string in ISO format. 

Format example: 
    - 2022-03-06T04:56:44.123456789 
    - 2022-03-06T04:56:44.000000000 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`str`</b>:  datetime string in YYYY-MM-DDTHH:MM:SS.mmmmmm format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_microseconds`

```python
to_microseconds(timestamp: ~TimestampType) → int
```

Converts timestamp to microseconds. 

If your timestamp has nanoseconds, they will be just cut (not rounding). 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`int`</b>:  Timestamp in microseconds format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_milliseconds`

```python
to_milliseconds(timestamp: ~TimestampType) → int
```

Converts timestamp to milliseconds. 

If your timestamp has nanoseconds, they will be just cut (not rounding). 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`int`</b>:  Timestamp in microseconds format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_nanoseconds`

```python
to_nanoseconds(timestamp: ~TimestampType) → int
```

Converts timestamp to nanoseconds. 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`int`</b>:  Timestamp in nanoseconds format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_seconds`

```python
to_seconds(timestamp: ~TimestampType)
```

Converts timestamp to seconds. 

If your timestamp has nanoseconds, they will be just cut (not rounding). 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`int`</b>:  Timestamp in seconds format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_th2_timestamp`

```python
to_th2_timestamp(timestamp: ~TimestampType) → dict
```

Converts timestamp to th2 timestamp. 



**Args:**
 
 - <b>`timestamp`</b>:  int object to convert. 



**Returns:**
 
 - <b>`dict`</b>:  {"epochSecond": seconds, "nano": nanoseconds} 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
