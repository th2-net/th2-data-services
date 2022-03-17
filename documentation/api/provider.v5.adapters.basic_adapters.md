<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.adapters.basic_adapters`






---

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AdapterGRPCObjectToDict`
GRPC Adapter decodes a GRPC object into a Dict object. 




---

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(record: Union[MessageData, EventData]) → dict
```

Decodes MessageData or EventData as GRPC object into a Dict object. 



**Args:**
 
 - <b>`record`</b>:  MessageData/EventData. 



**Returns:**
 Dict object. 


---

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AdapterSSE`
SSE Adapter handle bytes from sse-stream into Dict object. 




---

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(record: Event) → dict
```

SSE adapter. 



**Args:**
 
 - <b>`record`</b>:  SSE Event 



**Returns:**
 Dict object. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
