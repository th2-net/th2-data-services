from th2_data_services import Data

def test_break_iteration(demo_events_from_data_source: Data):
    iteratedOneItem = False
    for i,x in demo_events_from_data_source:
        if(iteratedOneItem):
            break
        iteratedOneItem=True

    count = 0

    for i,x in demo_events_from_data_source:
        count += 1

    assert count == 6 # length of demo_events_from_data_source