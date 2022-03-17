<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/stub_builder.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.stub_builder`






---

<a href="../../th2_data_services/provider/v5/stub_builder.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider5EventStubBuilder`




<a href="../../th2_data_services/provider/v5/stub_builder.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    event_struct=Provider5EventStruct(EVENT_ID='eventId', PARENT_EVENT_ID='parentEventId', STATUS='successful', NAME='eventName', TYPE='type', BATCH_ID='batchId', IS_BATCHED='isBatched', EVENT_TYPE='eventType', END_TIMESTAMP='endTimestamp', START_TIMESTAMP='startTimestamp', ATTACHED_MESSAGES_IDS='attachedMessageIds', BODY='body')
)
```

Event stub builder for Provider v5. 



**Args:**
 
 - <b>`event_struct`</b>:  Event struct class. 


---

#### <kbd>property</kbd> template

Event stub template. 



**Returns:**
  (dict) Event stub template. 




---

<a href="../../th2_data_services/provider/v5/stub_builder.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider5MessageStubBuilder`




<a href="../../th2_data_services/provider/v5/stub_builder.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    message_struct=Provider5MessageStruct(DIRECTION='direction', SESSION_ID='sessionId', MESSAGE_TYPE='messageType', CONNECTION_ID='connectionId', SESSION_ALIAS='sessionAlias', SUBSEQUENCE='subsequence', SEQUENCE='sequence', TIMESTAMP='timestamp', BODY='body', BODY_BASE64='bodyBase64', TYPE='type', MESSAGE_ID='messageId', ATTACHED_EVENT_IDS='attachedEventIds')
)
```

Event stub builder for Provider v5. 



**Args:**
 
 - <b>`message_struct`</b>:  Message struct class. 


---

#### <kbd>property</kbd> template

Message stub template. 



**Returns:**
  (dict) Message stub template. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
