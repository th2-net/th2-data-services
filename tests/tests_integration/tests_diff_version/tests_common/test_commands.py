def test_break_iteration_get_events(all_events):
    """TH2-4411 related test."""
    data = all_events.data

    for _ in data:
        break

    assert list(data) == all_events.expected_data_values


def test_break_iteration_get_messages(all_messages):
    """TH2-4411 related test."""
    data = all_messages.data
    for _ in data:
        break

    assert list(data) == all_messages.expected_data_values
