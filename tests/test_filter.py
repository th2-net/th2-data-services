from th2_data_services.filter import Filter


def test_filter_url():
    filter_ = Filter("type", ["one", 2, "three"], False, False)
    assert (
        filter_.url()
        == "&filters=type&type-values=one&type-values=2&type-values=three&type-negative=False&type-conjunct=False"
    )

    filter_ = Filter("name", "one", False, False)
    assert filter_.url() == "&filters=name&name-values=one&name-negative=False&name-conjunct=False"

    filter_ = Filter("name", 1)
    assert filter_.url() == "&filters=name&name-values=1&name-negative=False&name-conjunct=False"


def test_filter_grcp():
    assert isinstance(Filter("type", ["one", 2, "three"], False, False), Filter)


def test_iterate_filter_twice():
    f = Filter("type", ["one", 2, "three"])
    v1 = f.url()
    v2 = f.url()
    assert v1 == v2


def test_repr():
    f = Filter(name="type", values=["one", 2, "three"])
    assert repr(f) == "Filter(name='type', values=['one', '2', 'three'], negative='False', conjunct='False')"

    f = Filter(name="type", values="abc")
    assert repr(f) == "Filter(name='type', values=['abc'], negative='False', conjunct='False')"
