<!-- markdownlint-disable -->

<a href="../../th2_data_services/event_tree/etc_driver.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `event_tree.etc_driver`






---

<a href="../../th2_data_services/event_tree/etc_driver.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IETCDriver`




<a href="../../th2_data_services/event_tree/etc_driver.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    event_struct: IEventStruct,
    data_source: IDataSource,
    use_stub: bool = False
)
```

The driver for EventsTreeCollection and its inheritors. 



**Args:**
 
 - <b>`event_struct`</b>:  Structure of the event. 
 - <b>`data_source`</b>:  DataSource object. 
 - <b>`use_stub`</b>:  Build stubs or not. 




---

<a href="../../th2_data_services/event_tree/etc_driver.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build_stub_event`

```python
build_stub_event(id_: str) → ~Th2EventType
```

Builds stub event to generate parentless trees. 



**Args:**
 
 - <b>`id_`</b>:  Event Id. 

---

<a href="../../th2_data_services/event_tree/etc_driver.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event_id`

```python
get_event_id(event: ~Th2EventType)
```

Returns event id from the event. 

---

<a href="../../th2_data_services/event_tree/etc_driver.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event_name`

```python
get_event_name(event: ~Th2EventType)
```

Returns event name from the event. 

---

<a href="../../th2_data_services/event_tree/etc_driver.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_events_by_id_from_source`

```python
get_events_by_id_from_source(ids: Sequence) → list
```

Downloads the list of events from the provided data_source. 

---

<a href="../../th2_data_services/event_tree/etc_driver.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parent_event_id`

```python
get_parent_event_id(event: ~Th2EventType)
```

Returns parent event id from the event. 

---

<a href="../../th2_data_services/event_tree/etc_driver.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `stub_event_name`

```python
stub_event_name()
```

Returns stub event name. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
