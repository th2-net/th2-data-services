def test_findall_max_count(random_ETC):
    etc = random_ETC
    max_nodes_to_get = 10
    findall_nodes = etc.findall(filter=lambda e: e.get("parentEventId"), max_count=max_nodes_to_get)
    assert len(findall_nodes) == max_nodes_to_get


def test_findall_iter_max_count(random_ETC):
    etc = random_ETC
    one_value_from_findall = list(etc.findall_iter(filter=lambda e: e.get("parentEventId") is not None, max_count=1))
    assert [
        {"eventName": "Event D0", "eventId": "D0_id", "data": {"data": [63, 40, 40]}, "parentEventId": "root_id28"}
    ] == one_value_from_findall
