<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/data_source/http.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.data_source.http`




**Global Variables**
---------------
- **UNICODE_REPLACE_HANDLER**
- **TYPE_CHECKING**


---

<a href="../../th2_data_services/provider/v5/data_source/http.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HTTPProvider5DataSource`
DataSource class which provide work with rpt-data-provider. 

Rpt-data-provider version: 5.x.y Protocol: HTTP 

<a href="../../th2_data_services/provider/v5/data_source/http.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    url: 'str',
    chunk_length: 'int' = 65536,
    char_enc: 'str' = 'utf-8',
    decode_error_handler: 'str' = 'unicode_replace',
    event_struct: 'Provider5EventStruct' = Provider5EventStruct(EVENT_ID='eventId', PARENT_EVENT_ID='parentEventId', STATUS='successful', NAME='eventName', TYPE='type', BATCH_ID='batchId', IS_BATCHED='isBatched', EVENT_TYPE='eventType', END_TIMESTAMP='endTimestamp', START_TIMESTAMP='startTimestamp', ATTACHED_MESSAGES_IDS='attachedMessageIds', BODY='body'),
    message_struct: 'Provider5MessageStruct' = Provider5MessageStruct(DIRECTION='direction', SESSION_ID='sessionId', MESSAGE_TYPE='messageType', CONNECTION_ID='connectionId', SESSION_ALIAS='sessionAlias', SUBSEQUENCE='subsequence', SEQUENCE='sequence', TIMESTAMP='timestamp', BODY='body', BODY_BASE64='bodyBase64', TYPE='type', MESSAGE_ID='messageId', ATTACHED_EVENT_IDS='attachedEventIds'),
    event_stub_builder: 'IEventStub' = None,
    message_stub_builder: 'IMessageStub' = None,
    check_connect_timeout: '(int, float)' = 5
)
```

HTTPProvider5DataSource constructor. 



**Args:**
 
 - <b>`url`</b>:  HTTP data source url. 
 - <b>`check_connect_timeout`</b>:  How many seconds to wait for the server to send data before giving up. 
 - <b>`chunk_length`</b>:  How much of the content to read in one chunk. 
 - <b>`char_enc`</b>:  Encoding for the byte stream. 
 - <b>`decode_error_handler`</b>:  Registered decode error handler. 
 - <b>`event_struct`</b>:  Event structure that is supplied by rpt-data-provider. 
 - <b>`message_struct`</b>:  Message structure that is supplied by rpt-data-provider. 
 - <b>`event_stub_builder`</b>:  Stub builder for broken events. Provider5EventStubBuilder by default. 
 - <b>`message_stub_builder`</b>:  Stub builder for broken messages. Provider5MessageStubBuilder by default. 


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

HTTP Provider5 API. 

---

#### <kbd>property</kbd> url

str: URL of rpt-data-provider. 



---

<a href="../../th2_data_services/provider/v5/data_source/http.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `command`

```python
command(cmd: 'IHTTPProvider5Command')
```

HTTP Provider5 command processor. 



**Args:**
 
 - <b>`cmd`</b>:  The command of data source to execute. 



**Returns:**
 Data source command result. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
