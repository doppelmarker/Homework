from MarkKanaplianik.session2.task1_7.convert_tuple.convert_tuple import convert_tuple_to_integer


def test_convert_tuple_to_integer_positive01():
    t = (
        1,
        2,
        3,
        4,
    )

    expected = 1234

    actual = convert_tuple_to_integer(t)

    assert expected == actual


def test_convert_tuple_to_integer_positive02():
    t = (0, 0, 1, 9)

    expected = 19

    actual = convert_tuple_to_integer(t)

    assert expected == actual
