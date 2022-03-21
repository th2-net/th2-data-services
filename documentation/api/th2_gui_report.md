<!-- markdownlint-disable -->

<a href="../../th2_data_services/th2_gui_report.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `th2_gui_report`






---

<a href="../../th2_data_services/th2_gui_report.py#L1"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Th2GUIReport`
Class for creating gui link by event ID or message ID. 

<a href="../../th2_data_services/th2_gui_report.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(provider_link: str)
```

Th2GUIReport constructor. 



**Args:**
 
 - <b>`provider_link`</b> (str):  link to provider. 




---

<a href="../../th2_data_services/th2_gui_report.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event_link`

```python
get_event_link(event_id: str) → str
```

Creates the link with event id. 



**Args:**
 
 - <b>`event_id`</b> (str):  id for adding in link. 



**Returns:**
 GUI link to event. 

---

<a href="../../th2_data_services/th2_gui_report.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_message_link`

```python
get_message_link(message_id: str) → str
```

Creates the link with message id. 



**Args:**
 
 - <b>`message_id`</b> (str):  id for adding in link. 



**Returns:**
 GUI link to message. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
