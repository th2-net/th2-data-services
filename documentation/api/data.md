<!-- markdownlint-disable -->

<a href="../../th2_data_services/data.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `data`






---

<a href="../../th2_data_services/data.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Data`
A wrapper for data/data_stream. 

The class provides methods for working with data as a stream. 

Such approach to data analysis called........................................................ 

<a href="../../th2_data_services/data.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data:Optional[Iterator, Callable[, Generator[dict, NoneType]]],
    workflow:List[Dict[str, Union[Callable, str]]]=None,
    parents_cache:List[str]=None,
    instance_cache:bool=False,
    stream_cache:bool=False
)
```






---

#### <kbd>property</kbd> is_empty

bool: Indicates that the Data object doesn't contain data. 

---

#### <kbd>property</kbd> len

int: How many records in the Data stream. 



**Notes:**

> 1. It is a wasteful operation if you are performing it on the Data object that has never been iterated before. 
>2. If you want just to check emptiness, use is_empty property instead. 



---

<a href="../../th2_data_services/data.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `filter`

```python
filter(callback:Callable) → Data
```

Append `filter` to workflow. 



**Args:**
 
 - <b>`callback`</b>:  Filter function.  This function should return True or False.  If function returns False, the record will be removed from the dataflow. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find_by`

```python
find_by(record_field, field_values) → Generator
```

Get the records whose field value is written in the field_values list. 

When to use:  You have IDs of some messages and you want get them in the stream and stop searching  when you find all elements. 



**Args:**
 
 - <b>`record_field`</b>:  The record field to be searched for in the field_values list. 
 - <b>`field_values`</b>:  List of elements among which will be searched record[record_field]. 



**Yields:**
 
 - <b>`dict`</b>:  Generator records. 

---

<a href="../../th2_data_services/data.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_last_cache`

```python
get_last_cache() → Union[str, NoneType]
```

Returns last existing cache. 

Returns: Cache filename 

---

<a href="../../th2_data_services/data.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `limit`

```python
limit(num:int) → Data
```

Limits the stream to `num` entries. 



**Args:**
 
 - <b>`num`</b>:  How many records will be provided. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(callback:Callable) → Data
```

Append `transform` function to workflow. 



**Args:**
 
 - <b>`callback`</b>:  Transform function. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L294"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sift`

```python
sift(limit:int=None, skip:int=None) → Generator[dict, NoneType, NoneType]
```

Skips and limits records. 



**Args:**
 
 - <b>`limit`</b>:  Limited records. 
 - <b>`skip`</b>:  Skipped records. 



**Yields:**
 Generator records. 

---

<a href="../../th2_data_services/data.py#L317"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `use_cache`

```python
use_cache(status:bool) → Data
```

Change status instance_cache. 

If True all requested data from rpt-data-provider will be saved to instance_cache file. Further actions with Data object will be consume data from the instance_cache file. 



**Args:**
 
 - <b>`status`</b> (bool):  Status. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L359"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_to_file`

```python
write_to_file(file:str) → None
```

Writes the stream data to txt file. 



**Args:**
 
 - <b>`file`</b>:  Path to file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
