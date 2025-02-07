from th2_data_services.data import Data

file = "tests/tests_unit/test_data/test_from_json/file_with_unicode_symbols.jsonl"
data = Data.from_json(file)
file = "tests/tests_unit/test_data/test_from_json/file_with_unicode_symbols.jsonl.gz"
data = Data.from_json(file, gzip=True)

# ['{"Device Control Three val": "h\\nÁ␓`Å␒abc"}\r\n', '{"Device Control Three val": "h\\\\nÁ\\x13`Åx18abc"}\r\n'

# {"Device Control Three val": "h\\nÁ\x13`Åx18abc"}
# {"no_escape character in val": "\_abc"}
# {"\no_escape character in key": "_abc"}
# {"in_the_key_î": "abc"}
# {"in_the_val": "î_abc"}
# {"\tval": "\t_abc"}
# {"\nval": "\n_abc"}
def test_can_iterate_jsonl_file():
    pass
    # for x in data:
    #     print(x)

    # s = '{"Device Control Three val": "h\nÁ␓`Å␒abc"}'
    # import json
    # print(json.loads(s))
