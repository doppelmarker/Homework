from session2.task1_4.divisors.divisors import find_all_divisors


def test_find_all_divisors_positive01():
    n = 60

    expected = {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}

    actual = find_all_divisors(n)

    assert expected == actual


def test_find_all_divisors_positive02():
    n = 7

    expected = {1, 7}

    actual = find_all_divisors(n)

    assert expected == actual


def test_find_all_divisors_negative01():
    n = 8

    expected = {1, 2, 4}

    actual = find_all_divisors(n)

    assert expected != actual
