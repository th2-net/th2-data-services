<!-- markdownlint-disable -->

<a href="../../th2_data_services/data.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `data`






---

<a href="../../th2_data_services/data.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Data`
A wrapper for data/data_stream. 

The class provides methods for working with data as a stream. 

Such approach to data analysis called streaming transformation. 

<a href="../../th2_data_services/data.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Optional[Iterator, Callable[, Generator[~DataIterValues, NoneType]], List[Iterator]],
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

#### <kbd>property</kbd> metadata







---

<a href="../../th2_data_services/data.py#L714"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build_cache`

```python
build_cache(filename)
```

Creates cache file with provided name. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 

---

<a href="../../th2_data_services/data.py#L737"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_cache`

```python
clear_cache()
```

Clears related to data object cache file. 

This function won't remove external cache file. 

---

<a href="../../th2_data_services/data.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L630"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L796"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_any_file`

```python
from_any_file(filename, mode='r') → Data[str]
```

Creates Data object from any file with provided name. 

It will just iterate file and return data line be line. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to the file. 
 - <b>`mode`</b>:  Read mode of open function. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L748"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L820"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_csv`

```python
from_csv(
    filename,
    header=None,
    header_first_line=False,
    mode='r',
    delimiter=','
) → Data
```

Creates Data object from any file with provided name. 

It will iterate the CSV file as if you were doing it with CSV module. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to the file. 
 - <b>`header`</b>:  If provided header for csv, Data object will yield Dict[str]. 
 - <b>`header_first_line`</b>:  If the first line of the csv file is header, it'll take header from  the first line. Data object will yield Dict[str].  `header` argument is not required in this case. 
 - <b>`mode`</b>:  Read mode of open function. 
 - <b>`delimiter`</b>:  CSV file delimiter. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L770"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_json`

```python
from_json(filename, buffer_limit=250, gzip=False) → Data[dict]
```

Creates Data object from json file with provided name. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 
 - <b>`buffer_limit`</b>:  If limit is 0 buffer will not be used. Number of messages in buffer before parsing. 
 - <b>`gzip`</b>:  Set to true if file is json file compressed using gzip. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L309"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_cache_filepath`

```python
get_cache_filepath() → Path
```

Returns filepath for a cache file. 

---

<a href="../../th2_data_services/data.py#L305"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_pending_cache_filepath`

```python
get_pending_cache_filepath() → Path
```

Returns filepath for a pending cache file. 

---

<a href="../../th2_data_services/data.py#L552"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L480"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L592"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L929"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_json`

```python
to_json(filename: str, indent: int = None, overwrite: bool = False)
```

Converts data to json format. 



**Args:**
 
 - <b>`filename`</b> (str):  Output JSON filename 
 - <b>`indent`</b> (int, optional):  JSON format indent. Defaults to None. 
 - <b>`overwrite`</b> (bool, optional):  Overwrite if filename exists. Defaults to False. 



**Raises:**
 
 - <b>`FileExistsError`</b>:  If file exists and overwrite=False 

---

<a href="../../th2_data_services/data.py#L879"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_metadata`

```python
update_metadata(metadata: Dict) → Data
```

Update metadata of object with metadata argument. 

Metadata is updated with new values, meaning previous values are kept and added with new values. 

| Example: | data = Data(...) | # data.metadata => {'num': 1, 'nums': [1], 'letters': {'a': 97}} | new_metadata = {'num': 9, 'nums': [7], 'letters': {'z': 122}, 'new': 'key'} | data.update_metadata(new_metadata) | # data.metadata => {'num': 9, 'nums': [1,7], 'letters': {'a': 97, 'z': 122}, 'new': 'key'} 



**Args:**
 
 - <b>`metadata`</b> (dict):  New Metadata 



**Returns:**
 Data objects (itself) 



**Raises:**
 
 - <b>`Exception`</b>:  If metadata isn't dict, error will be raised. 
 - <b>`AttributeError`</b>:  If you're trying to update key value with dict which isn't a dict. 

---

<a href="../../th2_data_services/data.py#L615"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L656"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_to_file`

```python
write_to_file(file: str) → None
```

Writes the stream data to txt file. 



**Args:**
 
 - <b>`file`</b>:  Path to file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
