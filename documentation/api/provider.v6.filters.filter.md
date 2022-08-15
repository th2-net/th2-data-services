<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v6/filters/filter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v6.filters.filter`






---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider6Filter`
General interface for Filters of Provider v6. 

<a href="../../th2_data_services/provider/v6/filters/filter.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    name: str,
    values: Union[str, int, float, Sequence[Union[str, int, float]]],
    negative: bool = False,
    conjunct: bool = False
)
```

Filter constructor. 



**Args:**
 
 - <b>`name`</b> (str):  Filter name. 
 - <b>`values`</b> (Union[str, int, float, Sequence[Union[str, int, float]]]):  One string with filter value or list of filter values. 
 - <b>`negative`</b> (bool):   If true, will match events/messages that do not match those specified values.  If false, will match the events/messages by their values. Defaults to false. 
 - <b>`conjunct`</b> (bool):  If true, each of the specific filter values should be applied  If false, at least one of the specific filter values must be applied. 




---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → Filter
```

Generates the grpc object of the GRPC protocol API. 

---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Generates the filter part of the HTTP protocol API. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Generated filter. 


---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider6EventFilter`
Base class for Event Filters of Provider tests_v5. 

<a href="../../th2_data_services/provider/v6/filters/filter.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(values: Sequence[Any], negative: bool = False, conjunct: bool = False)
```








---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → Filter
```

Generates the grpc object of the GRPC protocol API. 

---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Generates the filter part of the HTTP protocol API. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Generated filter. 


---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Provider6MessageFilter`
Base class for Message Filters of Provider tests_v5. 

<a href="../../th2_data_services/provider/v6/filters/filter.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(values: Sequence[Any], negative: bool = False, conjunct: bool = False)
```








---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `grpc`

```python
grpc() → Filter
```

Generates the grpc object of the GRPC protocol API. 

---

<a href="../../th2_data_services/provider/v6/filters/filter.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Generates the filter part of the HTTP protocol API. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Generated filter. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
