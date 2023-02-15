<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/interfaces/data_source.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.interfaces.data_source`
Interfaces for Provider Data Source. 



---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IProviderDataSource`




<a href="../../th2_data_services/provider/interfaces/data_source.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    url: str,
    event_struct: IEventStruct,
    message_struct: IMessageStruct,
    event_stub_builder: IEventStub,
    message_stub_builder: IMessageStub
)
```

Interface of DataSource that provides work with rpt-data-provider. 



**Args:**
 
 - <b>`url`</b>:  Url address to data provider. 
 - <b>`event_struct`</b>:  Event struct class. 
 - <b>`message_struct`</b>:  Message struct class. 
 - <b>`event_stub_builder`</b>:  Event stub builder class. 
 - <b>`message_stub_builder`</b>:  Message stub builder class. 


---

#### <kbd>property</kbd> event_struct

Returns event structure class. 

---

#### <kbd>property</kbd> event_stub_builder

Returns event stub template. 

---

#### <kbd>property</kbd> message_struct

Returns message structure class. 

---

#### <kbd>property</kbd> message_stub_builder

Returns message stub template. 

---

#### <kbd>property</kbd> source_api

Returns Provider API. 

---

#### <kbd>property</kbd> url

str: URL of rpt-data-provider. 



---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `command`

```python
command(cmd: IProviderCommand)
```

Execute the transmitted command. 


---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IHTTPProviderDataSource`
Interface of DataSource that provides work with rpt-data-provider via HTTP. 

<a href="../../th2_data_services/provider/interfaces/data_source.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    url: str,
    event_struct: IEventStruct,
    message_struct: IMessageStruct,
    event_stub_builder: IEventStub,
    message_stub_builder: IMessageStub
)
```

Interface of DataSource that provides work with rpt-data-provider. 



**Args:**
 
 - <b>`url`</b>:  Url address to data provider. 
 - <b>`event_struct`</b>:  Event struct class. 
 - <b>`message_struct`</b>:  Message struct class. 
 - <b>`event_stub_builder`</b>:  Event stub builder class. 
 - <b>`message_stub_builder`</b>:  Message stub builder class. 


---

#### <kbd>property</kbd> event_struct

Returns event structure class. 

---

#### <kbd>property</kbd> event_stub_builder

Returns event stub template. 

---

#### <kbd>property</kbd> message_struct

Returns message structure class. 

---

#### <kbd>property</kbd> message_stub_builder

Returns message stub template. 

---

#### <kbd>property</kbd> source_api

Returns HTTP Provider API. 

---

#### <kbd>property</kbd> url

str: URL of rpt-data-provider. 



---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_connect`

```python
check_connect(
    timeout: (<class 'int'>, <class 'float'>),
    certification: bool = True
) → None
```

Checks whether url is working. 



**Args:**
 
 - <b>`timeout`</b>:  How many seconds to wait for the server to send data before giving up. 
 - <b>`certification`</b>:  Checking SSL certification. 



**Raises:**
 
 - <b>`urllib3.exceptions.HTTPError`</b>:  If unable to connect to host. 

---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `command`

```python
command(cmd: IHTTPProviderCommand)
```

Execute the transmitted HTTP command. 


---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IGRPCProviderDataSource`
Interface of DataSource that provides work with rpt-data-provider via GRPC. 

<a href="../../th2_data_services/provider/interfaces/data_source.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    url: str,
    event_struct: IEventStruct,
    message_struct: IMessageStruct,
    event_stub_builder: IEventStub,
    message_stub_builder: IMessageStub
)
```

Interface of DataSource that provides work with rpt-data-provider. 



**Args:**
 
 - <b>`url`</b>:  Url address to data provider. 
 - <b>`event_struct`</b>:  Event struct class. 
 - <b>`message_struct`</b>:  Message struct class. 
 - <b>`event_stub_builder`</b>:  Event stub builder class. 
 - <b>`message_stub_builder`</b>:  Message stub builder class. 


---

#### <kbd>property</kbd> event_struct

Returns event structure class. 

---

#### <kbd>property</kbd> event_stub_builder

Returns event stub template. 

---

#### <kbd>property</kbd> message_struct

Returns message structure class. 

---

#### <kbd>property</kbd> message_stub_builder

Returns message stub template. 

---

#### <kbd>property</kbd> source_api

Returns GRPC Provider API. 

---

#### <kbd>property</kbd> url

str: URL of rpt-data-provider. 



---

<a href="../../th2_data_services/provider/interfaces/data_source.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `command`

```python
command(cmd: IGRPCProviderCommand)
```

Execute the transmitted GRPC command. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
