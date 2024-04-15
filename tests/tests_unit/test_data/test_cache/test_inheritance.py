from typing import List


from tests.tests_unit.utils import (
    iterate_data_and_do_cache_checks,
    double_generator,
)

from th2_data_services.data import Data


# [2024.04.15] NOTE -- this test won't work more.
#   Reason:
#       It works when the Data source of the new Data obj is an old Data obj.
#       But now we added DataWorkflow class. It allows us to decrease overheads
#       on Data objects iterations.
#       This is especially noticeable when the Date object has a long forkflow
#       chain.
#   So it means that now, when we iterate a child Data object, which parent has
#       cache=True -> parent cache won't be created.
#
# def test_parent_cache_was_created(log_checker, general_data: List[dict]):
#     """
#     Issue related test: https://exactpro.atlassian.net/browse/TH2-3557
#
#     Cases:
#         [1] D(cache) -> D1(filter) -> D2(map) - creates D cache when you iterate D2.
#         [2] D(cache) -> D1(filter) -> D2(map + cache) - creates D and D2 cache files
#     """
#     # [1]
#     data = Data(general_data, cache=True)
#     data1 = data.filter(lambda record: record.get("isBatched"))
#     data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
#     iterate_data(data2)  # Just to iterate and create D cache file.
#     assert is_cache_file_exists(data)
#     # log_checker.cache_file_created(data)
#
#     # [2]
#     data = Data(general_data, cache=True)
#     data1 = data.filter(lambda record: record.get("isBatched"))
#     data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
#     data2.use_cache(True)
#     iterate_data(data2)  # Just to iterate and create cache files.
#     assert is_cache_file_exists(data)
#     assert is_cache_file_exists(data2)
#     # log_checker.cache_file_created(data)
#     # log_checker.cache_file_created(data2)


def test_data_iterates_parent_cache_file(log_checker, general_data: List[dict]):
    """D(cache) -> D1(filter) -> D2(map + cache) -> D3(filter) -> D4(map) - creates D and D2 cache files.
    There are 2 cache files, it should iterate D2 cache file.
    """

    def add_batch_status_to_dict_generator(stream):
        for record in stream:
            yield {**record, "batch-status": record.get("isBatched")}

    data = Data(general_data, cache=True)
    data1 = data.filter(lambda record: record.get("isBatched"))
    data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
    data2.use_cache(True)
    iterate_data_and_do_cache_checks(data2, log_checker)  # Just to iterate and create cache files.
    # log_checker.cache_file_created(data)

    data3 = data2.filter(lambda record: record.get("eventType"))
    data4 = data3.map_stream(double_generator)

    # Change D and D2 sources to [] to be aware data iterates cache file.
    data._data_source = ["D"]
    data2._data_source = ["D2"]
    assert len(list(data4)) == len(list(data3)) * 2
    # log_checker.used_own_cache_file(data2)


# [2024.04.15] NOTE -- this test won't work more.
#   Reason:
#       It works when the Data source of the new Data obj is an old Data obj.
#       But now we added DataWorkflow class. It allows us to decrease overheads
#       on Data objects iterations.
#       This is especially noticeable when the Date object has a long forkflow
#       chain.
#   So it means that now, when we iterate a child Data object, which parent has
#       cache=True -> parent cache won't be created.
#
# # @pytest.mark.xfail(reason="New methods return partial object which blocks knowing parent.")
# def test_cache_linear_inheritance(general_data: List[dict]):
#     """Cache file should be created for the first data object.
#
#     Issue related test: https://exactpro.atlassian.net/browse/TH2-3487
#     """
#     data = (
#         Data(general_data, cache=True)
#         .filter(lambda record: record.get("isBatched"))
#         .map(lambda record: {**record, "batch_status": record.get("isBatched")})
#     )
#     list(data)  # Just to iterate and create cache files.
#     assert is_cache_file_exists(data)


def test_cache_new_data_read_prev_data_cache(general_data: List[dict]):
    """
    Case: We create a Data obj.
    If the prev Data obj has cache file, the new Data object should read from
    this cache file.
    """
    expected_res_for_data_after_workflow = [
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint",
            "eventType": "Checkpoint",
            "isBatched": True,
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a4-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'th2-hand-demo' direction 'FIRST' "
            "sequence '1623852603564709030'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a6-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'SECOND' "
            "sequence '1624005475721015014'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a7-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc1' direction 'FIRST' "
            "sequence '1624005475720919499'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a8-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn2' direction 'FIRST' "
            "sequence '1624005448022245399'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a9-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn2' direction 'SECOND' "
            "sequence '1624005448022426113'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114aa-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'SECOND' "
            "sequence '1624005466840347015'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ab-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-dc2' direction 'FIRST' "
            "sequence '1624005466840263372'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ac-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-conn1' direction 'FIRST' "
            "sequence '1624005455622011522'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
            "batch_status": True,
            "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114ad-d1b4-11eb-9278-591e568ad66e",
            "eventName": "Checkpoint for session alias 'demo-log' direction 'FIRST' "
            "sequence '1624029363623063053'",
            "eventType": "Checkpoint for session",
            "isBatched": True,
            "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        },
        {
            "batchId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf",
            "batch_status": True,
            "eventId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf:8ca20288-d1b4-11eb-986f-1e8d42132387",
            "eventName": "Remove 'NewOrderSingle' "
            "id='demo-conn1:SECOND:1624005455622135205' "
            "Hash='7009491514226292581' Group='NOS_CONN' "
            "Hash['SecondaryClOrdID': 11111, 'SecurityID': INSTR1]",
            "eventType": "",
            "isBatched": True,
            "parentEventId": "a3779b94-d051-11eb-986f-1e8d42132387",
        },
    ]

    d1 = Data(general_data, cache=True)

    list(d1)  # Just to iterate and create cache files.
    d1._data_source = []

    # d1 should read cache
    assert list(d1) == general_data

    data = d1.filter(lambda record: record.get("isBatched")).map(
        lambda record: {**record, "batch_status": record.get("isBatched")}
    )

    # check that data reads cache file
    assert list(data) == expected_res_for_data_after_workflow

    d1.clear_cache()
    assert not d1.is_cache_file_exists()

    # If the source cache was removed, it should read the original source
    #   List in our case.
    d1._data_source = general_data
    assert list(data) == expected_res_for_data_after_workflow

    # assert is_cache_file_exists(data)
