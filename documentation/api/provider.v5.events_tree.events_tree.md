<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/events_tree/events_tree.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.events_tree.events_tree`






---

<a href="../../th2_data_services/provider/v5/events_tree/events_tree.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventsTreeProvider5`
EventsTree for data-provider v5. 

<a href="../../th2_data_services/provider/v5/events_tree/events_tree.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Iterable = None,
    tree: Tree = None,
    event_struct: IEventStruct = Provider5EventStruct(EVENT_ID='eventId', PARENT_EVENT_ID='parentEventId', STATUS='successful', NAME='eventName', TYPE='type', BATCH_ID='batchId', IS_BATCHED='isBatched', EVENT_TYPE='eventType', END_TIMESTAMP='endTimestamp', START_TIMESTAMP='startTimestamp', ATTACHED_MESSAGES_IDS='attachedMessageIds', BODY='body')
)
```

EventsTreeProvider5 constructor. 



**Args:**
 
 - <b>`data`</b>:  Iterable object. 
 - <b>`tree`</b>:  Tree. 
 - <b>`event_struct`</b>:  Event struct object. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
