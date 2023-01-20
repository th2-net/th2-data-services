<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.events_tree.exceptions`






---

<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventIdNotInTree`




<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id_)
```

Exception for the case when the tree hasn't the event. 



**Args:**
 
 - <b>`id_`</b>:  Event id. 





---

<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FieldIsNotExist`




<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(field_name)
```

Exception for the case when event as dict hasn't field. 



**Args:**
 
 - <b>`field_name`</b>:  Field name. 





---

<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventAlreadyExist`




<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_id)
```

Exception for the case when event already exist in tree. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 





---

<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventRootExist`




<a href="../../th2_data_services/interfaces/events_tree/exceptions.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_id)
```

Exception for the case when root already added in tree. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
