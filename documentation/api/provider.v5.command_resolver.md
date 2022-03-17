<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/command_resolver.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.command_resolver`





---

<a href="../../th2_data_services/provider/v5/command_resolver.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `resolver_get_event_by_id`

```python
resolver_get_event_by_id(
    data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource]
) → Union[GetEventById, GetEventById]
```

Resolves what 'GetEventById' command you need to use based Data Source. 



**Args:**
 
 - <b>`data_source`</b>:  DataSource instance. 



**Returns:**
 GetEventById command. 


---

<a href="../../th2_data_services/provider/v5/command_resolver.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `resolver_get_events_by_id`

```python
resolver_get_events_by_id(
    data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource]
) → Union[GetEventsById, GetEventsById]
```

Resolves what 'GetEventsById' command you need to use based Data Source. 



**Args:**
 
 - <b>`data_source`</b>:  DataSource instance. 



**Returns:**
 GetEventsById command. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
