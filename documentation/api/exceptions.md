<!-- markdownlint-disable -->

<a href="../../th2_data_services/exceptions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `exceptions`






---

<a href="../../th2_data_services/exceptions.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventNotFound`




<a href="../../th2_data_services/exceptions.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id_, error_description)
```

Exception for the case when the the event was not found in data source. 

**Args:**
 
 - <b>`id_`</b>:  Event id. 
 - <b>`error_description`</b>:  Description of error 





---

<a href="../../th2_data_services/exceptions.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MessageNotFound`




<a href="../../th2_data_services/exceptions.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id_, error_description)
```

Exception for the case when the the message was not found in data source. 

**Args:**
 
 - <b>`id_`</b>:  Event id. 
 - <b>`error_description`</b>:  Description of error 





---

<a href="../../th2_data_services/exceptions.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandError`
Exception raised for errors in the command. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._