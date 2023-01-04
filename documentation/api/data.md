<!-- markdownlint-disable -->

<a href="../../th2_data_services/data.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `data`






---

<a href="../../th2_data_services/data.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Data`
A wrapper for data/data_stream. 

The class provides methods for working with data as a stream. 

Such approach to data analysis called streaming transformation. 

<a href="../../th2_data_services/data.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Optional[Iterator, Callable[, Generator[dict, NoneType]], List[Iterator]],
    cache: bool = False,
    workflow: List[Dict[str, Union[Callable, str]]] = None
)
```

Data constructor. 



**Args:**
 
 - <b>`data`</b>:  Data source. Any iterable, Data object or a function that creates generator. 
 - <b>`cache`</b>:  Set True if you want to write and read from cache. 
 - <b>`workflow`</b>:  Workflow. 


---

#### <kbd>property</kbd> cache_status





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

<a href="../../th2_data_services/data.py#L644"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build_cache`

```python
build_cache(filename)
```

Creates cache file with provided name. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 

---

<a href="../../th2_data_services/data.py#L686"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_cache`

```python
clear_cache()
```

Clears related to data object cache file. 

This function won't remove external cache file. 

---

<a href="../../th2_data_services/data.py#L421"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `filter`

```python
filter(callback: Callable) → Data
```

Append `filter` to workflow. 



**Args:**
 
 - <b>`callback`</b>:  Filter function.  This function should return True or False.  If function returns False, the record will be removed from the dataflow. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L564"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L665"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_cache_file`

```python
from_cache_file(filename) → Data
```

Creates Data object from cache file with provided name. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileExistsError if provided file is not exist. 

---

<a href="../../th2_data_services/data.py#L282"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_cache_filepath`

```python
get_cache_filepath() → Path
```

Returns filepath for a cache file. 

---

<a href="../../th2_data_services/data.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_pending_cache_filepath`

```python
get_pending_cache_filepath() → Path
```

Returns filepath for a pending cache file. 

---

<a href="../../th2_data_services/data.py#L511"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `limit`

```python
limit(num: int) → Data
```

Limits the stream to `num` entries. 



**Args:**
 
 - <b>`num`</b>:  How many records will be provided. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(callback_or_adapter: Union[Callable, IRecordAdapter]) → Data
```

Append `transform` function to workflow. 



**Args:**
 
 - <b>`callback_or_adapter`</b>:  Transform function or an Adapter with IRecordAdapter interface implementation. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_stream`

```python
map_stream(
    adapter_or_generator: Union[IStreamAdapter, Callable[, Generator]]
) → Data
```

Append `stream-transform` function to workflow. 

If StreamAdapter is passed StreamAdapter.handle method will be used as a map function. 

Difference between map and map_stream: 1. map_stream allows you return None values. 2. map_stream allows you work with the whole stream but not with only 1 element, so you can implement some buffers inside handler. 3. map_stream works slightly efficent (faster on 5-10%). 



**Args:**
 
 - <b>`adapter_or_generator`</b>:  StreamAdapter object or generator function. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L526"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sift`

```python
sift(limit: int = None, skip: int = None) → Generator[dict, NoneType, NoneType]
```

Skips and limits records. 



**Args:**
 
 - <b>`limit`</b>:  Limited records. 
 - <b>`skip`</b>:  Skipped records. 



**Yields:**
 Generator records. 

---

<a href="../../th2_data_services/data.py#L549"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `use_cache`

```python
use_cache(status: bool = True) → Data
```

Changes cache flag and returns self. 



**Args:**
 
 - <b>`status`</b> (bool):  If True the whole data stream will be saved to cache file. Further actions with the Data object will consume data from the cache file. True by default. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L590"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_to_file`

```python
write_to_file(file: str) → None
```

Writes the stream data to txt file. 



**Args:**
 
 - <b>`file`</b>:  Path to file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
