from th2_data_services.filter import Filter


def test_filter_url():
    assert all(
        [
            Filter("type", ["one", 2, "three"], False, False).url()[1:]
            == "filters=type&type-values=one&type-values=2&type-values=three&type-negative=False",
            Filter("type", ["one", 2, "three"], True, True).url()[1:]
            == "filters=type&type-values=one&type-values=2&type-values=three&type-negative=True",
            Filter("type", ["one", 2, "three"], False, True).url()[1:]
            == "filters=type&type-values=one&type-values=2&type-values=three&type-negative=False",
            Filter("type", ["one", 2, "three"], True, False).url()[1:]
            == "filters=type&type-values=one&type-values=2&type-values=three&type-negative=True",
        ]
    )


def test_filter_grcp():
    assert isinstance(Filter("type", ["one", 2, "three"], False, False), Filter)
