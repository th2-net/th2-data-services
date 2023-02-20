<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.viewer_structs.verification`





---

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_comparison_line`

```python
format_comparison_line(field: Dict, failed_collection: bool = False) → str
```






---

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `check_if_verification_leaf_failed`

```python
check_if_verification_leaf_failed(leaf: Dict) → bool
```






---

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_body_verification`

```python
simplify_body_verification(body) → Dict
```






---

<a href="../../th2_data_services/utils/viewer_structs/verification.py#L139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_body_verification2`

```python
simplify_body_verification2(body) → Dict
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
