<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/json.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.json`






---

<a href="../../th2_data_services/utils/json.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BufferedJSONProcessor`




<a href="../../th2_data_services/utils/json.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(buffer_limit: int = 250)
```

BufferedJSONProcessor constructor. 



**Args:**
 
 - <b>`buffer_limit`</b>:  By default 250. If limit is 0 buffer will not be used. 




---

<a href="../../th2_data_services/utils/json.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fin`

```python
fin() → Generator
```

If buffer exists returns dicts from buffer. 



**Returns:**
  Generator[dict] 

---

<a href="../../th2_data_services/utils/json.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `from_buffer`

```python
from_buffer() → Generator
```

Transforms JSON objects to dict objects. 



**Returns:**
  Generator[dict] 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
