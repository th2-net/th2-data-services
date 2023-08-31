from th2_data_services.utils.converters import flatten_dict


def test_flatten_dict():
    rv = flatten_dict({"a": 1, "c": {"a": 2, "b": {"x": 5, "y": 10}}, "d": [1, 2, 3]})
    assert rv == {"a": 1, "c.a": 2, "c.b.x": 5, "c.b.y": 10, "d.0": 1, "d.1": 2, "d.2": 3}

    rv = flatten_dict(
        {"d": [{"a": 1, "c": {"z": 2, "b": [{"x": 5, "y": 10}, "str-in-lst"]}}, "str", 3]}
    )

    assert rv == {
        "d.0.a": 1,
        "d.0.c.z": 2,
        "d.0.c.b.0.x": 5,
        "d.0.c.b.0.y": 10,
        "d.0.c.b.1": "str-in-lst",
        "d.1": "str",
        "d.2": 3,
    }
