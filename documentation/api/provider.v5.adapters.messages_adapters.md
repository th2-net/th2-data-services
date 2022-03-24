<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/adapters/messages_adapters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.adapters.messages_adapters`






---

<a href="../../th2_data_services/provider/v5/adapters/messages_adapters.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AdapterDeleteMessageWrappers`
Adapter that delete unnecessary wrappers in events. 

It used for message to which an AdaptorGRPCObjectToDict has been applied. 

<a href="../../th2_data_services/provider/v5/adapters/messages_adapters.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    message_struct: Provider5MessageStruct = Provider5MessageStruct(DIRECTION='direction', SESSION_ID='sessionId', MESSAGE_TYPE='messageType', CONNECTION_ID='connectionId', SESSION_ALIAS='sessionAlias', SUBSEQUENCE='subsequence', SEQUENCE='sequence', TIMESTAMP='timestamp', BODY='body', BODY_BASE64='bodyBase64', TYPE='type', MESSAGE_ID='messageId', ATTACHED_EVENT_IDS='attachedEventIds')
)
```

AdapterDeleteMessageWrappers constructor. 



**Args:**
 
 - <b>`message_struct`</b>:  Message struct. 




---

<a href="../../th2_data_services/provider/v5/adapters/messages_adapters.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
