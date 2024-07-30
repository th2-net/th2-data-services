<!-- markdownlint-disable -->

<a href="../../th2_data_services/config/config.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `config.config`




**Global Variables**
---------------
- **options**


---

<a href="../../th2_data_services/config/config.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TH2Config`




<a href="../../th2_data_services/config/config.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__() → None
```

Global configuration for the DS library. 




---

<a href="../../th2_data_services/config/config.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `setup_resolvers`

```python
setup_resolvers(
    for_event: EventFieldResolver,
    for_message: MessageFieldResolver,
    for_submessage: SubMessageFieldResolver,
    for_expanded_message: ExpandedMessageFieldResolver
) → TH2Config
```

Use this to set up your custom resolvers. 



**Args:**
  for_event:  for_message:  for_submessage:  for_expanded_message: 



**Returns:**
  self 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
