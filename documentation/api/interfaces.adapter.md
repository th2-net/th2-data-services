<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/adapter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.adapter`






---

<a href="../../th2_data_services/interfaces/adapter.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IAdapter`
High level interface for Adapter. 




---

<a href="../../th2_data_services/interfaces/adapter.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(record: Any) → Any
```






---

<a href="../../th2_data_services/interfaces/adapter.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IMessageAdapter`
Interface of Adapter for messages. 




---

<a href="../../th2_data_services/interfaces/adapter.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(message: dict) → Any
```






---

<a href="../../th2_data_services/interfaces/adapter.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IEventAdapter`
Interface of Adapter for events. 




---

<a href="../../th2_data_services/interfaces/adapter.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(event: dict) → Any
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
