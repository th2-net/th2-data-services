<!-- markdownlint-disable -->

<a href="../../th2_data_services/th2_gui_report.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `th2_gui_report`






---

<a href="../../th2_data_services/th2_gui_report.py#L1"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Th2GUIReport`
Class for create gui link by event ID or message ID. 

<a href="../../th2_data_services/th2_gui_report.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(link_provider: str)
```

Th2GUIReport constructor. 



**Args:**
 
 - <b>`link_provider`</b> (str):  link to provider. 




---

<a href="../../th2_data_services/th2_gui_report.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_http`

```python
add_http(link: str)
```

Bringing links to a single form: add 'http://' to the beginning of the link. 



**Args:**
 
 - <b>`link`</b> (str):  link for editing. 



**Returns:**
 
 - <b>`link`</b> (str):  link with 'http://' in beginning. 

---

<a href="../../th2_data_services/th2_gui_report.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_slash`

```python
add_slash(link)
```

Bringing links to a single form: add '/' to the ending of the link. 



**Args:**
 
 - <b>`link`</b> (str):  link for editing. 



**Returns:**
 
 - <b>`link`</b> (str):  link with '/' in ending. 

---

<a href="../../th2_data_services/th2_gui_report.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event_link`

```python
get_event_link(event_id)
```

Create link with event id. 



**Args:**
 
 - <b>`event_id`</b> (str):  id for adding in link. 



**Returns:**
 Link with event id. 

---

<a href="../../th2_data_services/th2_gui_report.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_message_link`

```python
get_message_link(message_id)
```

Create link with message id. 



**Args:**
 
 - <b>`message_id`</b> (str):  id for adding in link. 



**Returns:**
 Link with message id. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
