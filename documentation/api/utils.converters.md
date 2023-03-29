<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/converters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.converters`






---

<a href="../../th2_data_services/utils/converters.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatetimeStringConverter`
Converts datetime strings. 

If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding). 

Expected timestamp format "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z". If you don't provide 'Z' in the end, it can return wrong results. 




---

<a href="../../th2_data_services/utils/converters.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(datetime_string: str) → (<class 'str'>, <class 'str'>)
```






---

<a href="../../th2_data_services/utils/converters.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatetimeConverter`
Converts datetime objects to timestamp. 

If you request milliseconds but your timestamp has microseconds, they will be just cut (not rounding). If you request nanoseconds, last 3 number will be zeros, because datatime object doesn't have nanoseconds. 

Expected timestamp format "datetime.datetime object". Expected that you provide UTC time in your data object. 




---

<a href="../../th2_data_services/utils/converters.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(datetime_obj: datetime) → (<class 'str'>, <class 'str'>)
```






---

<a href="../../th2_data_services/utils/converters.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProtobufTimestampConverter`
Converts Th2 timestamps. 

If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding). 

Expected timestamp format {'epochSecond': 123, 'nano': 500}. 




---

<a href="../../th2_data_services/utils/converters.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `parse_timestamp`

```python
parse_timestamp(timestamp: dict) → (<class 'str'>, <class 'str'>)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
