from th2_data_services import Data

def test_break_iteration_get_events(all_events):
    data = all_events.data
    iterated_one_item = False
    for _ in data:
        if iterated_one_item:
            break
        iterated_one_item = True

    count = 0

    for _ in data:
        count += 1

    assert count ==  len(all_events.expected_data_values)
1
def test_break_iteration_get_messages(all_messages):
    data = all_messages.data
    iterated_one_item = False
    for _ in data:
        if iterated_one_item:
            break
        iterated_one_item = True

    count = 0

    for _ in data:
        count += 1

    assert count == len(all_messages.expected_data_values)