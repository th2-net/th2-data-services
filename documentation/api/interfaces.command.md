<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/command.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.command`




**Global Variables**
---------------
- **TYPE_CHECKING**


---

<a href="../../th2_data_services/interfaces/command.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ICommand`
High level interface for Command. 




---

<a href="../../th2_data_services/interfaces/command.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: 'IDataSource')
```






---

<a href="../../th2_data_services/interfaces/command.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IAdaptableCommand`




<a href="../../th2_data_services/interfaces/command.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Class to make Command classes adaptable. 




---

<a href="../../th2_data_services/interfaces/command.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `apply_adapter`

```python
apply_adapter(adapter: 'Callable') → 'IAdaptableCommand'
```

Adds adapter to the Command workflow. 

Note, sequence that you will add adapters make sense. 



**Args:**
 
 - <b>`adapter`</b>:  Callable function that will be used as adapter. 

**Returns:**
 self 

---

<a href="../../th2_data_services/interfaces/command.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: 'IDataSource')
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
