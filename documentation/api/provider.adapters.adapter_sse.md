<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.adapters.adapter_sse`





---

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_default_sse_adapter`

```python
get_default_sse_adapter()
```






---

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SSEAdapter`
SSE Adapter handles bytes from sse-stream into Dict object. 

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(record: Event) → dict
```

Adapter handler. 



**Args:**
 
 - <b>`record`</b>:  SSE Event. 



**Returns:**
 Dict object. 


---

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `StreamingSSEAdapter`




<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(json_processor: BufferedJSONProcessor)
```








---

<a href="../../th2_data_services/provider/adapters/adapter_sse.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    record: (Generator[Event, NoneType, NoneType], Callable)
) → Generator[dict, NoneType, NoneType]
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
