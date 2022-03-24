<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/adapters/event_adapters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.adapters.event_adapters`






---

<a href="../../th2_data_services/provider/v5/adapters/event_adapters.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DeleteEventWrappersAdapter`
Adapter that deletes unnecessary wrappers in events. 

It used for events to which an AdaptorGRPCObjectToDict has been applied. 

<a href="../../th2_data_services/provider/v5/adapters/event_adapters.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    event_struct: Provider5EventStruct = Provider5EventStruct(EVENT_ID='eventId', PARENT_EVENT_ID='parentEventId', STATUS='successful', NAME='eventName', TYPE='type', BATCH_ID='batchId', IS_BATCHED='isBatched', EVENT_TYPE='eventType', END_TIMESTAMP='endTimestamp', START_TIMESTAMP='startTimestamp', ATTACHED_MESSAGES_IDS='attachedMessageIds', BODY='body')
)
```

AdapterDeleteEventWrappers constructor. 



**Args:**
 
 - <b>`event_struct`</b>:  Event struct. 




---

<a href="../../th2_data_services/provider/v5/adapters/event_adapters.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(event: dict) → dict
```

Deletes unnecessary wrappers for fields eventId, parentEventId and BatchId. 



**Args:**
 
 - <b>`event`</b>:  Event. 



**Returns:**
 Event without wrappers. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
