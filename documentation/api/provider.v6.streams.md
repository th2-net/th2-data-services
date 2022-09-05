<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v6/streams.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v6.streams`






---

<a href="../../th2_data_services/provider/v6/streams.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Streams`
General interface for composite streams of Provider v6. 

The class gives the opportunity to make list of streams with direction for each. 

<a href="../../th2_data_services/provider/v6/streams.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(streams: List[str], direction: str = None)
```

Streams constructor. 



**Args:**
 
 - <b>`streams`</b>:  List of Streams. 
 - <b>`direction`</b>:  Direction of Streams (Only FIRST or SECOND). If None then is both directions. 




---

<a href="../../th2_data_services/provider/v6/streams.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → List[MessageStream]
```

Generates the grpc objects of the GRPC protocol API. 



**Returns:**
 
 - <b>`List[MessageStream]`</b>:  List of Stream with specified direction. 

---

<a href="../../th2_data_services/provider/v6/streams.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Generates the stream part of the HTTP protocol API. 



**Returns:**
 
 - <b>`str`</b>:  Generated streams. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
