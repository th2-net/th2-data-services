<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.interfaces.filter`






---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider5Filter`




<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    name: str,
    values: Union[List[str], Tuple[str], str],
    negative: bool = False,
    conjunct: bool = False,
    exact: bool = False
)
```

Filter constructor. 



**Args:**
 
 - <b>`name`</b> (str):  Filter name. 
 - <b>`values`</b> (Union[List[str], Tuple[str], str]):  One string with filter value or list of filter values. 
 - <b>`negative`</b> (bool):   If true, will match events/messages that do not match those specified values.  If false, will match the events/messages by their values. Defaults to false. 
 - <b>`conjunct`</b> (bool):  If true, each of the specific filter values should be applied  If false, at least one of the specific filter values must be applied. 
 - <b>`exact`</b> (bool):  ..............  TODO 




---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → Filter
```





---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Forms a filter. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Formed filter. 


---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider5EventFilter`
Interface of command for rpt-data-provider. 

Rpt-data-provider version: 5.x.y Protocol: HTTP 

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    name: str,
    values: Union[List[str], Tuple[str], str],
    negative: bool = False,
    conjunct: bool = False,
    exact: bool = False
)
```

Filter constructor. 



**Args:**
 
 - <b>`name`</b> (str):  Filter name. 
 - <b>`values`</b> (Union[List[str], Tuple[str], str]):  One string with filter value or list of filter values. 
 - <b>`negative`</b> (bool):   If true, will match events/messages that do not match those specified values.  If false, will match the events/messages by their values. Defaults to false. 
 - <b>`conjunct`</b> (bool):  If true, each of the specific filter values should be applied  If false, at least one of the specific filter values must be applied. 
 - <b>`exact`</b> (bool):  ..............  TODO 




---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → Filter
```





---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Forms a filter. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Formed filter. 


---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider5MessageFilter`
Interface of command for rpt-data-provider. 

Rpt-data-provider version: 5.x.y Protocol: GRPC 

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    name: str,
    values: Union[List[str], Tuple[str], str],
    negative: bool = False,
    conjunct: bool = False,
    exact: bool = False
)
```

Filter constructor. 



**Args:**
 
 - <b>`name`</b> (str):  Filter name. 
 - <b>`values`</b> (Union[List[str], Tuple[str], str]):  One string with filter value or list of filter values. 
 - <b>`negative`</b> (bool):   If true, will match events/messages that do not match those specified values.  If false, will match the events/messages by their values. Defaults to false. 
 - <b>`conjunct`</b> (bool):  If true, each of the specific filter values should be applied  If false, at least one of the specific filter values must be applied. 
 - <b>`exact`</b> (bool):  ..............  TODO 




---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → Filter
```





---

<a href="../../th2_data_services/provider/v5/interfaces/filter.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Forms a filter. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Formed filter. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
