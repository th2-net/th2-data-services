from th2_data_services.data import Data

data = Data([1, 2, 3, 4, 5, 6, 7, 8])


def test_show_shows_more_than_default(capsys):
    n = 6
    data.show(n, idx_print=False)
    captured = capsys.readouterr()
    assert (
        captured.out
        == f"""------------- Printed first {n} records -------------
1
2
3
4
5
6
"""
    )


def test_show_shows_less_than_default(capsys):
    n = 2
    data.show(n, idx_print=False)
    captured = capsys.readouterr()
    assert (
        captured.out
        == f"""------------- Printed first {n} records -------------
1
2
"""
    )


# FIXME -- some issues with tests via pre-commit
# def test_show_extra_prints(capsys, general_data: List[dict]):
#     # First element is
#     x = {
#         "batchId": None,
#         "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
#         "eventName": "[TS_1]Aggressive IOC",
#         "eventType": "",
#         "isBatched": False,
#         "parentEventId": None,
#     }
#     n = 1
#     d1 = Data([x] + general_data)
#     d1.show(n, extra_prints={"isBatched": lambda e: "Yes" if e["isBatched"] else "No"})
#     captured = capsys.readouterr()
#     assert (
#         captured.out
#         == "------------- Printed first 1 records -------------\n[1] ------\nisBatched: No\n{'batchId': None,\n 'eventId': '84db48fc-d1b4-11eb-b0fb-199708acc7bc',\n 'eventName': '[TS_1]Aggressive IOC',\n 'eventType': '',\n 'isBatched': False,\n 'parentEventId': None}\n"
#     )


#     assert (
#         captured.out
#         == f"""------------- Printed first {n} records -------------
# [1] ------
# isBatched: No
# {{'batchId': None,
#  'eventId': '84db48fc-d1b4-11eb-b0fb-199708acc7bc',
#  'eventName': '[TS_1]Aggressive IOC',
#  'eventType': '',
#  'isBatched': False,
#  'parentEventId': None}}
# """
#     )
