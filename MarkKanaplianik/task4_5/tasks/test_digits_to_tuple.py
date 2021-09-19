from MarkKanaplianik.task4_5.digits_to_tuple.digits_to_tuple import get_tuple


def test_digits_to_tuple_positive01():
    numbers = 12345

    expected = (1, 2, 3, 4, 5)

    actual = get_tuple(numbers)

    assert expected == actual


def test_digits_to_tuple_positive02():
    numbers = 0

    expected = (0,)

    actual = get_tuple(numbers)

    assert expected == actual
