<!-- markdownlint-disable -->

<a href="../../th2_data_services/events_tree/parent_events_trees_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `events_tree.parent_events_trees_collection`






---

<a href="../../th2_data_services/events_tree/parent_events_trees_collection.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ParentEventsTreesCollection`
ParentEventsTreeCollections is a class like an EventsTreeCollections. 


- ParentEventsTree contains all parent events that are referenced. 
- Approximately for 1 million events will be ~23 thousand parent events. 

<a href="../../th2_data_services/events_tree/parent_events_trees_collection.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Data,
    data_source: IProviderDataSource = None,
    preserve_body: bool = False,
    event_stub_builder=None
)
```

ParentEventsTreesCollection constructor. 



**Args:**
 
 - <b>`data`</b>:  Data object. 
 - <b>`data_source`</b>:  Data Source object. 
 - <b>`preserve_body`</b>:  If True then save body of event. 
 - <b>`event_stub_builder`</b>:  Event Stub Builder. 


---

#### <kbd>property</kbd> detached_events

Gets detached events as dict with a view {'parent_id': ['referenced event', ...]}. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
