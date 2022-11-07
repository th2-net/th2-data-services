from th2_data_services import Data

def test_break_iteration_get_events(demo_events_from_data_source: Data):
    iterated_one_item = False
    for _ in demo_events_from_data_source:
        if iterated_one_item:
            break
        iterated_one_item = True

    count = 0

    for _ in demo_events_from_data_source:
        count += 1

    assert count == 6 # Length of demo_events_from_data_source

def test_break_iteration_get_messages(demo_messages_from_data_source: Data):
    iterated_one_item = False
    for _ in demo_messages_from_data_source:
        if iterated_one_item:
            break
        iterated_one_item = True

    count = 0

    for _ in demo_messages_from_data_source:
        count += 1

    assert count == 239 # Length of demo_messages_from_data_source