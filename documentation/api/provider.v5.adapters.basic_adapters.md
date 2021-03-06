<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.adapters.basic_adapters`






---

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GRPCObjectToDictAdapter`
GRPC Adapter decodes a GRPC object into a Dict object. 




---

<a href="../../th2_data_services/provider/v5/adapters/basic_adapters.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
