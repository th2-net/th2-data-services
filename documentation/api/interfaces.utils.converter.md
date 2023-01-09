<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/utils/converter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.utils.converter`






---

<a href="../../th2_data_services/interfaces/utils/converter.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ITimestampConverter`







---

<a href="../../th2_data_services/interfaces/utils/converter.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(timestamp: ~TimestampType) → (<class 'str'>, <class 'str'>)
```

Returns string representation of Unix time separated to seconds and nanoseconds. 

e.g. 2022-03-05T23:56:44.00123Z -> ('1646524604', '001230000') 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_datetime`

```python
to_datetime(timestamp: ~TimestampType) → datetime
```

Converts timestamp to datetime object. 

If your timestamp has nanoseconds, they will be just cut (not rounding). 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`datetime`</b>:  Timestamp in python datetime format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/utils/converter.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `to_milliseconds`

```python
to_milliseconds(timestamp: ~TimestampType)
```

Converts timestamp to milliseconds. 

If your timestamp has nanoseconds, they will be just cut (not rounding). 



**Args:**
 
 - <b>`timestamp`</b>:  TimestampType object to convert. 



**Returns:**
 
 - <b>`int`</b>:  Timestamp in microseconds format. 

---

<a href="../../th2_data_services/interfaces/utils/converter.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
