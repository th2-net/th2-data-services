<!-- markdownlint-disable -->

<a href="../../th2/data_services/event_tree/exceptions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `th2.data_services.event_tree.exceptions`






---

<a href="../../th2/data_services/event_tree/exceptions.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventIdNotInTree`




<a href="../../th2/data_services/event_tree/exceptions.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id_: str)
```

Exception for the case when the tree hasn't the event. 



**Args:**
 
 - <b>`id_`</b>:  Event id. 





---

<a href="../../th2/data_services/event_tree/exceptions.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FieldIsNotExist`




<a href="../../th2/data_services/event_tree/exceptions.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(field_name: str)
```

Exception for the case when event as dict hasn't field. 



**Args:**
 
 - <b>`field_name`</b>:  Field name. 





---

<a href="../../th2/data_services/event_tree/exceptions.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventAlreadyExist`




<a href="../../th2/data_services/event_tree/exceptions.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_id: str)
```

Exception for the case when event already exist in tree. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 





---

<a href="../../th2/data_services/event_tree/exceptions.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventRootExist`




<a href="../../th2/data_services/event_tree/exceptions.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_id: str)
```

Exception for the case when root already added in tree. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 





---

<a href="../../th2/data_services/event_tree/exceptions.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TreeLoop`




<a href="../../th2/data_services/event_tree/exceptions.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_id: str, parent_id: str)
```

Exception for the case when an event has link to a parent which is its descendant. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 
 - <b>`parent_id`</b>:  Parent id. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
