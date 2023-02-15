<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/message_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.message_utils`





---

<a href="../../th2_data_services/utils/message_utils.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `expand_message`

```python
expand_message(message: Dict) → List[Dict]
```

Extract compounded message into list of individual messages. 



**Args:**
 
 - <b>`message`</b>:  TH2-Message 



**Returns:**
 List[Dict] 


---

<a href="../../th2_data_services/utils/message_utils.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_totals`

```python
get_totals(
    messages: List[Dict],
    categorizers: List[Callable],
    filter_: Callable = None
) → Dict[str, int]
```

Returns dictionary quantities of events for different message categories. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`categorizers`</b>:  List of categorizer functions 
 - <b>`filter_`</b>:  Filter functon, defaults to None 



**Returns:**
 Dict[str, int] 


---

<a href="../../th2_data_services/utils/message_utils.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_totals`

```python
print_totals(
    messages: List[Dict],
    categorizers: List[Callable],
    filter_: Callable = None
) → None
```

Prints dictionary quantities of events for different message categories. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`categorizers`</b>:  List of categorizer functions 
 - <b>`filter_`</b>:  Filter functon, defaults to None 


---

<a href="../../th2_data_services/utils/message_utils.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_some`

```python
get_some(
    messages: List[Dict],
    max_count: int,
    start: int = 0,
    filter_: Callable = None
) → List[Dict]
```

Returns limited list of messages from the stream. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`max_count`</b>:  Maximum messages to retrieve 
 - <b>`start`</b>:  Extract events starting form this number, defaults to 0 
 - <b>`filter_`</b>:  Filter function, defaults to None 



**Returns:**
 List[Dict] 


---

<a href="../../th2_data_services/utils/message_utils.py#L145"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_some_raw`

```python
print_some_raw(
    messages: List[Dict],
    max_count: int,
    start: int = 0,
    filter_: Callable = None
) → None
```

Prints limited list of messages from the stream in dictionary format. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`max_count`</b>:  Maximum messages to retrieve 
 - <b>`start`</b>:  Extract events starting form this number, defaults to 0 
 - <b>`filter_`</b>:  Filter function, defaults to None 


---

<a href="../../th2_data_services/utils/message_utils.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_some_raw_source`

```python
print_some_raw_source(
    messages: List[Dict],
    max_count: int,
    start: int = 0,
    filter_: Callable = None
) → None
```

Prints limited list of messages from the stream in ascii from raw binary format. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`max_count`</b>:  Maximum messages to retrieve 
 - <b>`start`</b>:  Extract events starting form this number, defaults to 0 
 - <b>`filter_`</b>:  Filter function, defaults to None 


---

<a href="../../th2_data_services/utils/message_utils.py#L191"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_some`

```python
print_some(
    messages: List[Dict],
    max_count: int,
    start: int = 0,
    filter_: Callable = None
) → None
```

Prints limited list of messages from the stream in dictionary format. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`max_count`</b>:  Maximum messages to retrieve 
 - <b>`start`</b>:  Extract events starting form this number, defaults to 0 
 - <b>`filter_`</b>:  Filter function, defaults to None 


---

<a href="../../th2_data_services/utils/message_utils.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `message_fields_to_flat_dict`

```python
message_fields_to_flat_dict(message: Dict, result: Dict, prefix: str)
```






---

<a href="../../th2_data_services/utils/message_utils.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `message_to_dict`

```python
message_to_dict(message: Dict)
```

Converts message body to dict. 



**Args:**
 
 - <b>`message`</b>:  TH2-Message 



**Returns:**
 Dict 


---

<a href="../../th2_data_services/utils/message_utils.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_time`

```python
extract_time(message: Dict) → str
```

Extracts timestamp from message. 



**Args:**
 
 - <b>`message`</b>:  TH2-Message 



**Returns:**
 str 


---

<a href="../../th2_data_services/utils/message_utils.py#L258"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_message`

```python
print_message(message: Dict) → None
```

Print message (verbose). 



**Args:**
 
 - <b>`message`</b>:  TH2-Message 


---

<a href="../../th2_data_services/utils/message_utils.py#L273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_raw_body_str`

```python
get_raw_body_str(m)
```






---

<a href="../../th2_data_services/utils/message_utils.py#L283"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_message_raw_source`

```python
print_message_raw_source(message: Dict) → None
```






---

<a href="../../th2_data_services/utils/message_utils.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `resolve_count_message_ids`

```python
resolve_count_message_ids(messages: List[Dict], ids: Set) → None
```

Resolves set of message IDs. # TODO: Update Description. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`ids`</b>:  Set of messages IDs to resolve 



**Returns:**
 None, Modifies `ids` 


---

<a href="../../th2_data_services/utils/message_utils.py#L317"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `resolve_message_ids`

```python
resolve_message_ids(messages: List[Dict], ids: Set) → Dict[str, Dict]
```

Resolves set of message IDs. # TODO: Update Description. 



**Args:**
 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`ids`</b>:  Set of messages IDs to resolve 



**Returns:**
 Dict[str, Dict] 


---

<a href="../../th2_data_services/utils/message_utils.py#L338"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_category_frequencies`

```python
get_category_frequencies(
    messages: List[Dict],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = 'seconds',
    filter_: Callable = None
)
```






---

<a href="../../th2_data_services/utils/message_utils.py#L358"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_category_frequencies`

```python
print_category_frequencies(
    messages: List[Dict],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = 'seconds',
    filter_: Callable = None,
    return_html=False
) → Union[NoneType, str]
```






---

<a href="../../th2_data_services/utils/message_utils.py#L378"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_messages_examples`

```python
get_messages_examples(
    messages: List[Dict],
    categories: List[str],
    categorizer: Callable,
    filter_: Callable = None
) → Dict
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
