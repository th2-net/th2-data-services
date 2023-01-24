# TODO - these tests will fail when demo_etc_with_data will have More than 1 tree
#   and max_count > than number of events that were found in the first tree.
#
# TODO - WE HAVE TO CREATE SUCH TEST and FIX issue

# TODO - I've found this error when have ETC(trees=100, [events=100])

# def test_findall_max_count(demo_etc_with_data, general_data):
#     etc = demo_etc_with_data
#     one_value_from_findall = etc.findall(filter=lambda e: e["parentEventId"] is not None,
#                                          max_count=10)
#     assert 10 == len(one_value_from_findall)
#
#
# def test_findall_iter_max_count(demo_etc_with_data, general_data):
#     etc = demo_etc_with_data
#     one_value_from_findall = list(etc.findall_iter(filter=lambda e: e["parentEventId"] is not None, max_count=1))
#     assert [{
#             "batchId": None,
#             "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
#             "eventName": "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for " "instrument INSTR1",
#             "eventType": "",
#             "isBatched": False,
#             "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
#         }] == one_value_from_findall
