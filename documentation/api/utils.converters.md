<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/converters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.converters`






---

<a href="../../th2_data_services/utils/converters.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatetimeStringConverter`
Converts datetime strings. 

If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding). 

Expected timestamp format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z". 




---

<a href="../../th2_data_services/utils/converters.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(datetime_string: str) → (<class 'str'>, <class 'str'>)
```






---

<a href="../../th2_data_services/utils/converters.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatetimeConverter`
Converts datetime objects to timestamp. 

If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding). 

Expected datetime object shouldn't contain microseconds. 




---

<a href="../../th2_data_services/utils/converters.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(datetime_obj: datetime) → (<class 'str'>, <class 'str'>)
```






---

<a href="../../th2_data_services/utils/converters.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProtobufTimestampConverter`
Converts Th2 timestamps. 

If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding). Expected timestamp format {'epochSecond': 123, 'nano': 500}. 




---

<a href="../../th2_data_services/utils/converters.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(timestamp: dict) → (<class 'str'>, <class 'str'>)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
