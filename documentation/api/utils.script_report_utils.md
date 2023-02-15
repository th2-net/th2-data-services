<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/script_report_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.script_report_utils`




**Global Variables**
---------------
- **ver_dict**
- **tree_table**

---

<a href="../../th2_data_services/utils/script_report_utils.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tag_rows_to_flat_dict`

```python
tag_rows_to_flat_dict(collection: Dict, flat_list: Dict, prefix: str) → None
```

rows are used in 'Tree table', 'Table'  but not in the Verification (uses fields) 



**Args:**
 
 - <b>`collection`</b>:  'Tree table' or 'Table' 
 - <b>`flat_list`</b>:  NOT a list - dict. Used just to put result to this object. prefix: 



**Returns:**
 


---

<a href="../../th2_data_services/utils/script_report_utils.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_comparison_line`

```python
format_comparison_line(field: Dict, failed_collection: bool = False) → str
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `verification_fields_to_flat_dict`

```python
verification_fields_to_flat_dict(
    collection: Dict,
    flat_list: Dict,
    prefix,
    failed_collection: bool = False
)
```

If a field A has a sub-field B, dot notation sting will be returned. 



**Examples:**
  failed_collection=False  {'hzField A': '   value [*]',  'hzField B': '!  2531410 [2531410]',  'hzSub message A.Field C': ' # 9 [9]'} 

 failed_collection=True  {'hzField A': ' # value [*]',  'hzField B': '!# 2531410 [2531410]',  'hzSub message A.Field C': ' # 9 [9]'} 



**Args:**
 
 - <b>`collection`</b>:  verification collection like here https://exactpro.atlassian.net/wiki/spaces/TH2/pages/63766549/rpt-viewer+supported+event+content#Verification 
 - <b>`flat_list`</b>:  NOT a list - dict. Used just to put result to this object. 
 - <b>`prefix`</b>:  prefix that will be added before each field name. 
 - <b>`failed_collection`</b>:  ??? 



**Returns:**
 


---

<a href="../../th2_data_services/utils/script_report_utils.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `check_if_verification_leaf_failed`

```python
check_if_verification_leaf_failed(leaf: Dict) → bool
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `verification_fields_to_simple_dict`

```python
verification_fields_to_simple_dict(
    collection: Dict,
    parent: Dict,
    failed_collection: bool = False
) → None
```



**Examples:**
  failed_collection=False  {'Field A': '   value [*]',  'Field B': '!  2531410 [2531410]',  '# Sub message A': {'Field C': ' # 9 [9]'}} 

 failed_collection=True  {'Field A': ' # value [*]',  'Field B': '!# 2531410 [2531410]',  '# Sub message A': {'Field C': ' # 9 [9]'}} 



**Args:**
 
 - <b>`collection`</b>:  verification collection like here https://exactpro.atlassian.net/wiki/spaces/TH2/pages/63766549/rpt-viewer+supported+event+content#Verification 
 - <b>`parent`</b>:  NOT a list - dict. Used just to put result to this object. 
 - <b>`failed_collection`</b>:  ?? 



**Returns:**
 


---

<a href="../../th2_data_services/utils/script_report_utils.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `item_status_fail`

```python
item_status_fail(str_irem) → bool
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L196"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_body_outgoing_message`

```python
simplify_body_outgoing_message(body) → Dict
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_body_verification`

```python
simplify_body_verification(body) → Dict
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L216"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_body_verification2`

```python
simplify_body_verification2(body) → Dict
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_body_tree_table_list`

```python
simplify_body_tree_table_list(body) → Dict
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `enrich_events_tree_with_attached_messages`

```python
enrich_events_tree_with_attached_messages(index, messages, filter_lambda) → Dict
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_child_by_type`

```python
find_child_by_type(leaf: Dict, type: str) → List
```

Finds child by type. 



**Args:**
 
 - <b>`leaf`</b>:  Child leaf 
 - <b>`type`</b>:  Type to match 



**Returns:**
 List 


---

<a href="../../th2_data_services/utils/script_report_utils.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_child_by_types`

```python
find_child_by_types(leaf, types)
```

Finds child by type. 



**Args:**
 
 - <b>`leaf`</b>:  Child leaf 
 - <b>`types`</b>:  List of types to match 



**Returns:**
 List 


---

<a href="../../th2_data_services/utils/script_report_utils.py#L304"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `id_tags`

```python
id_tags() → List[str]
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `defining_tags`

```python
defining_tags() → List[str]
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L338"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_expected_event`

```python
format_expected_event(expected_event_str: str, alias_by_id: Dict) → str
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L346"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_actual_event`

```python
format_actual_event(actual_message_dict, actual_message_str, alias_by_id)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L363"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_corresponding_missing_filter`

```python
find_corresponding_missing_filter(expectation_string, verifications_list)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L396"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_corresponding_verification`

```python
find_corresponding_verification(
    expectation_string,
    verifications_list,
    already_used_verifications_set
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L424"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_step_request_id`

```python
process_step_request_id(request_tags, alias_by_id, custom_id_tags)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L448"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_val_from_verification`

```python
get_val_from_verification(formatted_val)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L456"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_ids_from_dict`

```python
extract_ids_from_dict(
    fields,
    is_this_request,
    is_this_verification,
    custom_id_tags,
    r_result,
    i_result
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L473"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `matrix_model_test_case_analyze_ids`

```python
matrix_model_test_case_analyze_ids(report_leaf, custom_id_tags)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L504"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `matrix_model_test_case_processor`

```python
matrix_model_test_case_processor(report_leaf)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L675"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_generic_tree_and_index`

```python
generate_generic_tree_and_index(events, parents_filter)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L688"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_generic_tree_and_index_from_parents_list`

```python
generate_generic_tree_and_index_from_parents_list(events, parents)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L706"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_model_matrix_tree_and_index`

```python
generate_model_matrix_tree_and_index(events, parents_filter, extra=None)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L720"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_matrix_json_report_limited_batches`

```python
generate_matrix_json_report_limited_batches(
    events,
    reports_path,
    parents_filter,
    par_btch_len,
    extra=None
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L731"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extra_post_processor`

```python
extra_post_processor(main_processor, extra_processor)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L736"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_generic_json_report_limited_batches`

```python
generate_generic_json_report_limited_batches(
    events,
    reports_path,
    parents_filter,
    par_btch_len,
    post_processors_dict=None
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L771"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_generic_json_report`

```python
generate_generic_json_report(
    events,
    reports_path,
    parents_filter,
    one_file=False
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L777"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_model_matrix_json_report`

```python
generate_model_matrix_json_report(
    events,
    reports_path,
    parents_filter,
    one_file=False
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L792"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `collect_element`

```python
collect_element(p, l, elements_to_collect, collected_data)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L807"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_parallel_tables`

```python
create_parallel_tables(story_item, collected_data)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L838"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `collect_ids_for_story`

```python
collect_ids_for_story(story_items_list, smart, events, messages)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L865"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_story`

```python
prepare_story(
    story_items_list,
    json_path=None,
    events=None,
    event_body_processors=None,
    messages=None
)
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L1012"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `test_verification_fields_to_flat_dict`

```python
test_verification_fields_to_flat_dict()
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L1029"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `test_verification_fields_to_simple_dict`

```python
test_verification_fields_to_simple_dict()
```






---

<a href="../../th2_data_services/utils/script_report_utils.py#L1046"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `test_simplify_body_tree_table_list`

```python
test_simplify_body_tree_table_list()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
