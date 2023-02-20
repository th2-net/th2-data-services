<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/interfaces/command.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.interfaces.command`
Interfaces for Provider Commands. 

**Global Variables**
---------------
- **TYPE_CHECKING**


---

<a href="../../th2_data_services/provider/interfaces/command.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IProviderCommand`
Interface of command for rpt-data-provider. 




---

<a href="../../th2_data_services/provider/interfaces/command.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: 'IProviderDataSource')
```






---

<a href="../../th2_data_services/provider/interfaces/command.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IHTTPProviderCommand`
Interface of command for rpt-data-provider which works via HTTP. 




---

<a href="../../th2_data_services/provider/interfaces/command.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: 'IHTTPProviderDataSource')
```






---

<a href="../../th2_data_services/provider/interfaces/command.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IGRPCProviderCommand`
Interface of command for rpt-data-provider which works via GRPC. 




---

<a href="../../th2_data_services/provider/interfaces/command.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: 'IGRPCProviderDataSource')
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
