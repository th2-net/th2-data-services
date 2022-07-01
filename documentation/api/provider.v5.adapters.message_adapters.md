<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.adapters.message_adapters`






---

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DeleteMessageWrappersAdapter`
Adapter that deletes unnecessary wrappers in messages. 

It used for the message to which an AdaptorGRPCObjectToDict has been applied. 

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    message_struct: Provider5MessageStruct = Provider5MessageStruct(DIRECTION='direction', SESSION_ID='sessionId', MESSAGE_TYPE='messageType', CONNECTION_ID='connectionId', SESSION_ALIAS='sessionAlias', SUBSEQUENCE='subsequence', SEQUENCE='sequence', TIMESTAMP='timestamp', BODY='body', BODY_BASE64='bodyBase64', TYPE='type', MESSAGE_ID='messageId', ATTACHED_EVENT_IDS='attachedEventIds', LOOKUP_LIMIT_DAYS='lookup_limit_days')
)
```

AdapterDeleteMessageWrappers constructor. 



**Args:**
 
 - <b>`message_struct`</b>:  Message struct. 




---

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(message: dict) → dict
```

Deletes unnecessary wrappers for field message_id. 



**Args:**
 
 - <b>`message`</b>:  Message. 



**Returns:**
 Message without wrappers. 


---

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CodecPipelinesAdapter`
Adapter for codec-pipeline messages from provider v5. 

Codec-pipeline messages have sub-messages in the body. This adapter used for split codec-pipeline message to separate messages. 

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ignore_errors=False)
```

AdapterCodecPipelines constructor. 



**Args:**
 
 - <b>`ignore_errors`</b>:  If True it will ignore errors and return message as is. 




---

<a href="../../th2_data_services/provider/v5/adapters/message_adapters.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(message: dict) → Union[List[dict], dict]
```

Adapter handler. 



**Args:**
 
 - <b>`message`</b>:  Th2Message dict. 



**Returns:**
 Th2Message dict. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
