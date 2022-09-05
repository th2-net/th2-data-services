from tests.tests_unit.tests_diff_version.conftest import Filter


def test_repr():
    f = Filter(name="type", values=["one", 2, "three"])
    assert repr(f) == "Filter(name='type', values=['one', '2', 'three'], negative='False', conjunct='False')"

    f = Filter(name="type", values="abc")
    assert repr(f) == "Filter(name='type', values=['abc'], negative='False', conjunct='False')"
