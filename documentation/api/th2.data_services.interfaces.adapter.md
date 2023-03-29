<!-- markdownlint-disable -->

<a href="../../th2/data_services/interfaces/adapter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `th2.data_services.interfaces.adapter`






---

<a href="../../th2/data_services/interfaces/adapter.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IStreamAdapter`
Interface of Adapter for streams. 




---

<a href="../../th2/data_services/interfaces/adapter.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(stream: Iterable) → Any
```

Stream handle function that should yield data (not return). 


---

<a href="../../th2/data_services/interfaces/adapter.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IRecordAdapter`
Interface of Adapter for record. 




---

<a href="../../th2/data_services/interfaces/adapter.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(record: dict) → Any
```

One record handle function that should return data. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
