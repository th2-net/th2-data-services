<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/misc_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.misc_utils`





---

<a href="../../th2_data_services/utils/misc_utils.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_stats_dict`

```python
print_stats_dict(d: dict)
```






---

<a href="../../th2_data_services/utils/misc_utils.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_time`

```python
extract_time(data: dict, type_: str = 'event') → str
```

Extracts Time From TH2-Event/Message. 



**Args:**
 
 - <b>`data`</b> (dict):  TH2-Event/Message 
 - <b>`type_`</b> (str, optional):  Event/Message Identifier. Defaults to 'e'. 
 - <b>`Aliases`</b>:  Event - [e, ev, event], Message - [m, msg, message] 



**Returns:**
 
 - <b>`str`</b>:  "timestampEpoch.nanoSeconds" 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
