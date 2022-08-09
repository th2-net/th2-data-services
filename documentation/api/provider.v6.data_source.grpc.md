<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v6/data_source/grpc.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v6.data_source.grpc`




**Global Variables**
---------------
- **TYPE_CHECKING**


---

<a href="../../th2_data_services/provider/v6/data_source/grpc.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GRPCProvider6DataSource`
DataSource class which provide work with rpt-data-provider. 

Rpt-data-provider version: 6.x.y Protocol: GRPC 

<a href="../../th2_data_services/provider/v6/data_source/grpc.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    url: 'str',
    event_struct: 'IEventStruct' = Provider6EventStruct(EVENT_ID='eventId', PARENT_EVENT_ID='parentEventId', STATUS='successful', NAME='eventName', TYPE='type', BATCH_ID='batchId', IS_BATCHED='isBatched', EVENT_TYPE='eventType', END_TIMESTAMP='endTimestamp', START_TIMESTAMP='startTimestamp', ATTACHED_MESSAGES_IDS='attachedMessageIds', BODY='body'),
    message_struct: 'IMessageStruct' = Provider6MessageStruct(DIRECTION='direction', SESSION_ID='sessionId', MESSAGE_TYPE='messageType', CONNECTION_ID='connectionId', SESSION_ALIAS='sessionAlias', SUBSEQUENCE='subsequence', SEQUENCE='sequence', TIMESTAMP='timestamp', BODY='body', BODY_BASE64='bodyBase64', TYPE='type', MESSAGE_ID='messageId', ATTACHED_EVENT_IDS='attachedEventIds'),
    event_stub_builder: 'IEventStub' = Provider6EventStubBuilder,
    message_stub_builder: 'IMessageStub' = Provider6MessageStubBuilder
)
```

GRPCProvider6DataSource constructor. 



**Args:**
 
 - <b>`url`</b>:  Url of rpt-data-provider. 
 - <b>`event_struct`</b>:  Event structure that is supplied by rpt-data-provider. 
 - <b>`message_struct`</b>:  Message structure that is supplied by rpt-data-provider. 
 - <b>`event_stub_builder`</b>:  Stub builder for broken events. 
 - <b>`message_stub_builder`</b>:  Stub builder for broken messages. 


---

#### <kbd>property</kbd> event_struct

Returns event structure class. 

---

#### <kbd>property</kbd> event_stub_builder

Returns event stub template. 

---

#### <kbd>property</kbd> message_struct

Returns message structure class. 

---

#### <kbd>property</kbd> message_stub_builder

Returns message stub template. 

---

#### <kbd>property</kbd> source_api

Returns Provider API. 

---

#### <kbd>property</kbd> url

str: URL of rpt-data-provider. 



---

<a href="../../th2_data_services/provider/v6/data_source/grpc.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `command`

```python
command(cmd: 'IGRPCProvider6Command') → Any
```

Execute the transmitted GRPC command. 



**Args:**
 
 - <b>`cmd`</b>:  GRPC Command. 



**Returns:**
 
 - <b>`Any`</b>:  Command response. 



**Raises:**
 
 - <b>`CommandError`</b>:  If the command was broken. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
