<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/stub_builder.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.stub_builder`






---

<a href="../../th2_data_services/interfaces/stub_builder.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IStub`




<a href="../../th2_data_services/interfaces/stub_builder.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Stab interface. 


---

#### <kbd>property</kbd> template







---

<a href="../../th2_data_services/interfaces/stub_builder.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build`

```python
build(fields: dict) → dict
```

Builds a stub by template. 

All keys will be overwrited by fields. New keys from fields will be added to stub. 



**Args:**
 
 - <b>`fields`</b>:  Fields that will overwrite template. 



**Returns:**
 Stub dict. 



**Raises:**
 
 - <b>`TypeError`</b>:  If required fields is absent in changed fields list. 


---

<a href="../../th2_data_services/interfaces/stub_builder.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IEventStub`
Just to mark Event Stub class. 

<a href="../../th2_data_services/interfaces/stub_builder.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Stab interface. 


---

#### <kbd>property</kbd> template







---

<a href="../../th2_data_services/interfaces/stub_builder.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build`

```python
build(fields: dict) → dict
```

Builds a stub by template. 

All keys will be overwrited by fields. New keys from fields will be added to stub. 



**Args:**
 
 - <b>`fields`</b>:  Fields that will overwrite template. 



**Returns:**
 Stub dict. 



**Raises:**
 
 - <b>`TypeError`</b>:  If required fields is absent in changed fields list. 


---

<a href="../../th2_data_services/interfaces/stub_builder.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IMessageStub`
Just to mark Message Stub class. 

<a href="../../th2_data_services/interfaces/stub_builder.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Stab interface. 


---

#### <kbd>property</kbd> template







---

<a href="../../th2_data_services/interfaces/stub_builder.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build`

```python
build(fields: dict) → dict
```

Builds a stub by template. 

All keys will be overwrited by fields. New keys from fields will be added to stub. 



**Args:**
 
 - <b>`fields`</b>:  Fields that will overwrite template. 



**Returns:**
 Stub dict. 



**Raises:**
 
 - <b>`TypeError`</b>:  If required fields is absent in changed fields list. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
