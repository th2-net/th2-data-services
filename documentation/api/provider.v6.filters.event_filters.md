<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v6.filters.event_filters`






---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TypeFilter`
Will match the events which type contains one of the given substrings. 





---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `NameFilter`
Will match the events which name contains one of the given substrings. 





---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BodyFilter`
Will match the events which body contains one of the given substrings. 





---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AttachedMessageIdFilter`
Filters the events that are linked to the specified message id. 





---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PassedStatusFilter`
Will match the events which status equals passed. 

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `url`

```python
url() → str
```

Generates the filter part of the HTTP protocol API. 

For help use this readme: https://github.com/th2-net/th2-rpt-data-provider#filters-api. 



**Returns:**
 
 - <b>`str`</b>:  Generated filter. 


---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FailedStatusFilter`
Will match the events which status equals failed. 

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../th2_data_services/provider/v6/filters/event_filters.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
