<!-- markdownlint-disable -->

<a href="../../th2_data_services/data.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `data`






---

<a href="../../th2_data_services/data.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Data`
A wrapper for data/data_stream. 

The class provides methods for working with data as a stream. 

Such approach to data analysis called streaming transformation. 

<a href="../../th2_data_services/data.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Optional[Iterator, Callable[, Generator[~DataIterValues, NoneType]], List[Iterable], Iterable],
    cache: bool = False,
    workflow: List[Dict[str, Union[Callable, str]]] = None,
    pickle_version: int = 4
)
```

Data constructor. 



**Args:**
 
 - <b>`data`</b>:  Data source. Any iterable, Data object or a function that creates generator. 
 - <b>`cache`</b>:  Set True if you want to write and read from cache. 
 - <b>`workflow`</b>:  DataWorkflow. 
 - <b>`pickle_version`</b>:  Pickle protocol version. Set if using cache. 


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

<a href="../../th2_data_services/data.py#L817"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build_cache`

```python
build_cache(filename)
```

Creates cache file with provided name. 

Important:  If the Data object cache status is True, it'll iterate itself. As a result the cache file  will be created and copied.  When you will iterate the Data object next time, it'll iterate created cache file. 

 NOTE! If you build cache file, Data.cache_status was False and after that you'll set  Data.cache_status == TRUE -- the Data object WON'T iterate build file because it doesn't  keep the path to built cache file.. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 

---

<a href="../../th2_data_services/data.py#L859"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_cache`

```python
clear_cache()
```

Clears related to data object cache file. 

This function won't remove external cache file. 

---

<a href="../../th2_data_services/data.py#L443"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L668"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L817"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_any_file`

```python
from_any_file(filename, mode='r') → Data[str]
```

Creates a Data object from any file with the provided name. 

It will just iterate file and return data line be line. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to the file. 
 - <b>`mode`</b>:  Read mode of open function. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L868"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_cache_file`

```python
from_cache_file(filename, pickle_version: int = 4) → Data
```

Creates Data object from cache file with provided name. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 
 - <b>`pickle_version`</b>:  Pickle protocol version. Change default value  if your pickle file was created with another pickle version. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L940"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>


### <kbd>classmethod</kbd> `from_csv`

```python
from_csv(
    filename: Union[str, Path],
    header=None,
    header_first_line=False,
    mode='r',
    delimiter=','
) → Data
```

Creates Data object from CSV file with provided name. 

It will iterate the CSV file as if you were doing it with CSV module. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to the file. 
 - <b>`header`</b>:  If provided header for csv, Data object will yield Dict[str].  Note, if your first line is header in csv, it also will be yielded. 
 - <b>`header_first_line`</b>:  If the first line of the csv file is header,  it'll take header from the first line. Data object will yield  Dict[str]. `header` argument is not required in this case.  First line of the CSV file will be skipped (header line). 
 - <b>`mode`</b>:  Read mode of open function. 
 - <b>`delimiter`</b>:  CSV file delimiter. 



**Note:**

> If `header` provided and `header_first_line == True`, Data object will yield Dict[str] where key names (columns) as described in the `header`. First line of the CSV file will be skipped. 
>

**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L894"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_json`

```python
from_json(filename, buffer_limit=250, gzip=False) → Data[dict]
```

Creates Data object from json-lines file with provided name. 



**Args:**
 
 - <b>`filename`</b>:  Name or path to cache file. 
 - <b>`buffer_limit`</b>:  If limit is 0 buffer will not be used. Number of messages in buffer before parsing. 
 - <b>`gzip`</b>:  Set to true if file is json file compressed using gzip. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 



**Raises:**
 FileNotFoundError if provided file does not exist. 

---

<a href="../../th2_data_services/data.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_cache_filepath`

```python
get_cache_filepath() → Path
```

Returns filepath for a cache file. 

---

<a href="../../th2_data_services/data.py#L317"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_pending_cache_filepath`

```python
get_pending_cache_filepath() → Path
```

Returns filepath for a pending cache file. 

---

<a href="../../th2_data_services/data.py#L642"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_sorted`

```python
is_sorted(get_timestamp_func: Callable[[Any], Any]) → IsSortedResult
```

Checks whether Data is sorted. 



**Args:**
 
 - <b>`get_timestamp_func`</b>:  This function is responsible for getting the timestamp. 



**Returns:**
 
 - <b>`IsSortedResult`</b>:  Whether data is sorted and additional info (e.g. index of the first unsorted element). 

---

<a href="../../th2_data_services/data.py#L579"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L477"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(callback_or_adapter: Union[Callable, IRecordAdapter]) → Data
```

Append `transform` function to workflow. 



**Args:**
 
 - <b>`callback_or_adapter`</b>:  Transform function or an Adapter with IRecordAdapter  interface implementation.  If the function returns None value, this value will be skipped from OUT stream.  If you don't want skip None values -- use `map_stream`. 



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

Difference between map and map_stream: 1. map_stream allows you return None values. 2. map_stream allows you work with the whole stream but not with only 1 element,  so you can implement some buffers inside handler. 3. map_stream works slightly efficient (faster on 5-10%). 



**Args:**
 
 - <b>`adapter_or_generator`</b>:  StreamAdapter object or generator function. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L537"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_yield`

```python
map_yield(callback_or_adapter: Union[Callable, IRecordAdapter])
```

Maps the stream using callback function or adapter. 

Differences between map and map yield: 1. map_yield is a wrapper function using map_stream. 2. map_yield iterates over each item in record if callback return value is a list or tuple. 



**Args:**
 
 - <b>`callback_or_adapter`</b>:  Transform function or an Adapter with IRecordAdapter interface implementation. 



**Returns:**
 
 - <b>`Data`</b>:  Data object. 

---

<a href="../../th2_data_services/data.py#L619"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L1066"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_json`

```python
to_json(filename: Union[str, Path], indent: int = None, overwrite: bool = False)
```

Converts data to valid json format. 



**Args:**
 
 - <b>`filename`</b> (str):  Output JSON filename 
 - <b>`indent`</b> (int, optional):  JSON format indent. Defaults to None. 
 - <b>`overwrite`</b> (bool, optional):  Overwrite if filename exists. Defaults to False. 



**NOTE:**

> Data object can iterate not only dicts. So not every data can be saved as json. 
>

**Raises:**
 
 - <b>`FileExistsError`</b>:  If file exists and overwrite=False 

---

<a href="../../th2_data_services/data.py#L1125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_json_lines`

```python
to_json_lines(
    filename: Union[str, Path],
    indent: int = None,
    overwrite: bool = False,
    gzip: bool = False,
    compresslevel: int = 5
)
```

Converts Data to json lines. 

Every line is a valid json, but the whole file - not. 



**Args:**
 
 - <b>`filename`</b> (str):  Output JSON filename. 
 - <b>`indent`</b> (int, optional):  DON'T used now. 
 - <b>`overwrite`</b> (bool, optional):  Overwrite if filename exists. Defaults to False. 
 - <b>`gzip`</b>:  Set to True if you want to compress the file using gzip. 
 - <b>`compresslevel`</b>:  gzip compression level. 



**NOTE:**

> Data object can iterate not only dicts. So not every data can be saved as json. 
>

**Raises:**
 
 - <b>`FileExistsError`</b>:  If file exists and overwrite=False 

---

<a href="../../th2_data_services/data.py#L1004"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_jsons`

```python
to_jsons(
    filename: Union[str, Path],
    indent: int = None,
    overwrite: bool = False,
    gzip=False,
    compresslevel=5
)
```

[DEPRECATED] Converts data to json lines. 

Every line is a valid json, but the whole file - not. 



**Args:**
 
 - <b>`filename`</b> (str):  Output JSON filename. 
 - <b>`indent`</b> (int, optional):  DON'T used now. 
 - <b>`overwrite`</b> (bool, optional):  Overwrite if filename exists. Defaults to False. 
 - <b>`gzip`</b>:  Set to True if you want to compress the file using gzip. 
 - <b>`compresslevel`</b>:  gzip compression level. 



**Raises:**
 
 - <b>`FileExistsError`</b>:  If file exists and overwrite=False 

---

<a href="../../th2_data_services/data.py#L995"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_metadata`

```python
update_metadata(metadata: Dict) → Data
```

Update metadata of object with metadata argument. 

Metadata is updated with new values, meaning previous values are kept and added with new values. 

| Example: | data = Data(...) | # data.metadata => {'num': 1, 'nums': [1], 'letters': {'a': 97}} | new_metadata = {'num': 9, 'nums': [7], 'letters': {'z': 122}, 'new': 'key'} | data.update_metadata(new_metadata) | # data.metadata => {'num': 9, 'nums': [1,7], 'letters': {'a': 97, 'z': 122}, 'new': 'key'} 

If at least one value with is a list in one Data object, update_metadata adds both values in a list. 

| Example: | data = Data(...) | # data.metadata => {'str_example_one': ['str1'], 'str_example_two': 'str1'} | new_metadata = {'str_example_one': 'str2', 'str_example_two': ['str2']} | data.update_metadata(new_metadata) | # data.metadata => {'str_example_one': ['str1', 'str2'], 'str_example_two': ['str1', 'str2']} 



**Args:**
 
 - <b>`metadata`</b> (dict):  New Metadata 



**Returns:**
 Data objects (itself) 



**Raises:**
 
 - <b>`Exception`</b>:  If metadata isn't dict, error will be raised. 
 - <b>`AttributeError`</b>:  If you're trying to update key value with dict which isn't a dict. 

---

<a href="../../th2_data_services/data.py#L653"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/data.py#L694"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_to_file`

```python
write_to_file(file: str) → None
```

Writes the stream data to txt file. 



**Args:**
 
 - <b>`file`</b>:  Path to file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
