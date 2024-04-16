from th2_data_services.data_source import lwdp  # to init resolvers
from th2_data_services.utils import message_utils


def test_message_get_category_frequencies_5s(
    messages_frequencies_test_data, messages_frequencies_expected_values_5s
):
    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="5s",
        gap_mode=1,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_5s["GAP_1_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="5s",
        gap_mode=2,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_5s["GAP_2_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="5s",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_5s["GAP_3_ANCHOR_FALSE_LEN"] == len(list(table))

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="5s",
        gap_mode=2,
        zero_anchor=True,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_5s["GAP_2_ANCHOR_TRUE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="5s",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_5s["GAP_3_ANCHOR_TRUE_LEN"] == len(list(table))


def test_message_get_category_frequencies_1h(
    messages_frequencies_test_data, messages_frequencies_expected_values_1h
):
    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="1h",
        gap_mode=1,
        zero_anchor=False,
        object_expander=None,
    )
    print(list(table))
    print(messages_frequencies_expected_values_1h["GAP_1_ANCHOR_FALSE"])
    assert messages_frequencies_expected_values_1h["GAP_1_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="1h",
        gap_mode=2,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_1h["GAP_2_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="1h",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_1h["GAP_3_ANCHOR_FALSE_LEN"] == len(list(table))

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="1h",
        gap_mode=2,
        zero_anchor=True,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_1h["GAP_2_ANCHOR_TRUE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="1h",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_1h["GAP_3_ANCHOR_TRUE_LEN"] == len(list(table))


def test_message_get_category_frequencies_2h(
    messages_frequencies_test_data, messages_frequencies_expected_values_2h
):
    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2h",
        gap_mode=1,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2h["GAP_1_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2h",
        gap_mode=2,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2h["GAP_2_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2h",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2h["GAP_3_ANCHOR_FALSE_LEN"] == len(list(table))

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2h",
        gap_mode=2,
        zero_anchor=True,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2h["GAP_2_ANCHOR_TRUE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2h",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2h["GAP_3_ANCHOR_TRUE_LEN"] == len(list(table))


def test_message_get_category_frequencies_2d(
    messages_frequencies_test_data, messages_frequencies_expected_values_2d
):
    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2d",
        gap_mode=1,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2d["GAP_1_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2d",
        gap_mode=2,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2d["GAP_2_ANCHOR_FALSE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2d",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2d["GAP_3_ANCHOR_FALSE_LEN"] == len(list(table))

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2d",
        gap_mode=2,
        zero_anchor=True,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2d["GAP_2_ANCHOR_TRUE"] == list(table)

    table = message_utils.frequencies.get_category_frequencies(
        messages_frequencies_test_data,
        [],
        lambda a: a["messageType"],
        aggregation_level="2d",
        gap_mode=3,
        zero_anchor=False,
        object_expander=None,
    )
    assert messages_frequencies_expected_values_2d["GAP_3_ANCHOR_TRUE_LEN"] == len(list(table))
