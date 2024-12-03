"""
The data tested on looks as follows:
    
a2321a5b-f883-11ec-8225-52540095fac0
--a261010a-f883-11ec-8c42-52540095fac0
----bd118950-f883-11ec-bb81-b900dc34ec7b
------bdbae8c1-f883-11ec-bb81-b900dc34ec7b
"""
WARNINGNAME = "PROBLEM CASE"

# TODO
#   Remake to work with new version of ETC

# data_source = HTTPProvider5DataSource("http://10.100.66.114:31787/")
#
# events: Data = data_source.command(
#     commands.GetEventsById(['30491fae-f885-11ec-bf0f-bd5660c0cda6',
#                             '4c118cfc-f885-11ec-bf0f-bd5660c0cda6'])
# )
#
#
# def testcase1():
#     '''
#     Case 1
#     2nd and 4th generation in data present
#     Warning case
#     '''
#     events: Data = data_source.command(
#         commands.GetEventsById(['a261010a-f883-11ec-8c42-52540095fac0',
#                                 'bdbae8c1-f883-11ec-bb81-b900dc34ec7b'])
#     )
#
#     with warnings.catch_warnings(record=True) as w:
#         ETC = EventsTreeCollectionProvider5(events, data_source=data_source)
#
#     assert [warning for warning in w if str(warning.message) == WARNINGNAME]
#
#
# def testcase2():
#     '''
#     Case 2
#     3nd and 4th generation in data present
#     Not a warning case
#     '''
#     events: Data = data_source.command(
#         commands.GetEventsById(['bd118950-f883-11ec-bb81-b900dc34ec7b',
#                                 'bdbae8c1-f883-11ec-bb81-b900dc34ec7b'])
#     )
#
#     with warnings.catch_warnings(record=True) as w:
#         ETC = EventsTreeCollectionProvider5(events, data_source=data_source)
#
#     assert [warning for warning in w if
#             str(warning.message) == WARNINGNAME] == []
#
#
# def testcase3():
#     '''
#     Case 3
#     root and 4th generation in data present
#     Warning case
#     '''
#     events: Data = data_source.command(
#         commands.GetEventsById(['a2321a5b-f883-11ec-8225-52540095fac0',
#                                 'bdbae8c1-f883-11ec-bb81-b900dc34ec7b'])
#     )
#
#     with warnings.catch_warnings(record=True) as w:
#         ETC = EventsTreeCollectionProvider5(events, data_source=data_source)
#
#     assert [warning for warning in w if str(warning.message) == WARNINGNAME]
