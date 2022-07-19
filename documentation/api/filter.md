<!-- markdownlint-disable -->

<a href="../../th2_data_services/filter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `filter`






---

<a href="../../th2_data_services/filter.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Filter`
The class for using rpt-data-provider filters API. 

<a href="../../th2_data_services/filter.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    name: str,
    values: Sequence[str],
    negative: bool = False,
    conjunct: bool = False
)
```

Filter constructor. 



**Args:**
 
 - <b>`name`</b> (str):  Filter name. 
 - <b>`values`</b> (Union[List[str], Tuple[str], str]):  One string with filter value or list of filter values. 
 - <b>`negative`</b> (bool):   If true, will match events/messages that do not match those specified values.  If false, will match the events/messages by their values. Defaults to false. 
 - <b>`conjunct`</b> (bool):  If true, each of the specific filter values should be applied  If false, at least one of the specific filter values must be applied. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
