<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/sse_client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.sse_client`






---

<a href="../../th2_data_services/utils/sse_client.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SSEClient`
Patch for sseclient-py to get availability to configure decode error handler. 

<a href="../../th2_data_services/utils/sse_client.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_source, char_enc='utf-8', decode_errors_handler='strict')
```

Initialize the SSE client over an existing, ready to consume event source. 

The event source is expected to be a binary stream and have a close() method. That would usually be something that implements io.BinaryIOBase, like an httplib or urllib3 HTTPResponse object. 




---

<a href="../../th2_data_services/utils/sse_client.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `events`

```python
events()
```

Returns events in generator style. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
