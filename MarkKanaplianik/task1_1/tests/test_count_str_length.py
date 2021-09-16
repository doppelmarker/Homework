from MarkKanaplianik.task1_1.str_length.count_str_length import count_str_length


def test_count_str_length_positive01():
    string = "abcde"

    expected_length = 5

    actual_length = count_str_length(string)

    assert expected_length == actual_length


def test_count_str_length_positive02():
    string = ""

    expected_length = 0

    actual_length = count_str_length(string)

    assert expected_length == actual_length


def test_count_str_length_negative01():
    string = "1234"

    expected_length = 3

    actual_length = count_str_length(string)

    assert expected_length != actual_length
