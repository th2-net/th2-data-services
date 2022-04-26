<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/events_tree/parent_events_tree_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.events_tree.parent_events_tree_collection`






---

<a href="../../th2_data_services/provider/v5/events_tree/parent_events_tree_collection.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ParentEventsTreeCollectionProvider5`
ParentEventsTreeCollection for data-provider v5. 

<a href="../../th2_data_services/provider/v5/events_tree/parent_events_tree_collection.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Data,
    data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource] = None,
    preserve_body: bool = False,
    event_struct: IEventStruct = Provider5EventStruct(EVENT_ID='eventId', PARENT_EVENT_ID='parentEventId', STATUS='successful', NAME='eventName', TYPE='type', BATCH_ID='batchId', IS_BATCHED='isBatched', EVENT_TYPE='eventType', END_TIMESTAMP='endTimestamp', START_TIMESTAMP='startTimestamp', ATTACHED_MESSAGES_IDS='attachedMessageIds', BODY='body'),
    stub: bool = False
)
```

ParentEventsTreeCollectionProvider5 constructor. 



**Args:**
 
 - <b>`data`</b>:  Data object. 
 - <b>`data_source`</b>:  Data Source object. 
 - <b>`preserve_body`</b>:  If True it will preserve 'body' field in the Events. 
 - <b>`event_struct`</b>:  Event struct object. 
 - <b>`stub`</b>:  If True it will create stub when event is broken. 


---

#### <kbd>property</kbd> detached_events

Gets detached events as dict with a view {'parent_id': ['referenced event', ...]}. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
