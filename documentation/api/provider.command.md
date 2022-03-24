<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/command.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.command`






---

<a href="../../th2_data_services/provider/command.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProviderAdaptableCommand`




<a href="../../th2_data_services/provider/command.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Class to make Command classes adaptable. 




---

<a href="../../th2_data_services/provider/command.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `apply_adapter`

```python
apply_adapter(adapter: 'Callable') → 'ProviderAdaptableCommand'
```

Adds adapter to the Command workflow. 

Note, sequence that you will add adapters make sense. 



**Args:**
 
 - <b>`adapter`</b>:  Callable function that will be used as adapter. 



**Returns:**
 self 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
