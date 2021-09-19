from MarkKanaplianik.task4_3.custom_split.custom_split import custom_split


def test_custom_split_whitespaces_mode_limitless():
    s = " 1   2 3       4  "

    assert str.split(s) == custom_split(s)


def test_custom_split_whitespaces_mode_negative_limit():
    s = " 1   2 3       4  "
    maxsplit = -2

    assert str.split(s, maxsplit=maxsplit) == custom_split(s, maxsplit=maxsplit)


def test_custom_split_whitespaces_mode_limit_0():
    s = " 1   2 3       4  "
    maxsplit = 0

    assert str.split(s, maxsplit=maxsplit) == custom_split(s, maxsplit=maxsplit)


def test_custom_split_whitespaces_mode_limit_1():
    s = " 1   2 3       4  "
    maxsplit = 1

    assert str.split(s, maxsplit=maxsplit) == custom_split(s, maxsplit=maxsplit)


def test_custom_split_normal_mode_sep_by_whitespace_limitless():
    s = " 1   2 3       4  "
    sep = " "

    assert str.split(s, sep) == custom_split(s, sep)


def test_custom_split_normal_mode_sep_by_whitespace_negative_limit():
    s = " 1   2 3       4  "
    sep = " "
    maxsplit = -2

    assert str.split(s, sep, maxsplit) == custom_split(s, sep, maxsplit)


def test_custom_split_normal_mode_sep_by_whitespace_limit_0():
    s = " 1   2 3       4  "
    sep = " "
    maxsplit = 0

    assert str.split(s, sep, maxsplit) == custom_split(s, sep, maxsplit)


def test_custom_split_normal_mode_sep_by_whitespace_limit_1():
    s = " 1   2 3       4  "
    sep = " "
    maxsplit = 1

    assert str.split(s, sep, maxsplit) == custom_split(s, sep, maxsplit)


def test_custom_split_normal_mode_sep_by_comma_limit_1():
    s = "1,2,3,4"
    sep = ","
    maxsplit = 1

    assert str.split(s, sep, maxsplit) == custom_split(s, sep, maxsplit)


def test_custom_split_normal_mode_sep_by_comma_where_comma_leading_and_preceding_limit_3():
    s = ",1,2,3,4,"
    sep = ","
    maxsplit = 3

    assert str.split(s, sep, maxsplit) == custom_split(s, sep, maxsplit)


def test_custom_split_whitespaces_mode_empty_string():
    s = ""

    assert str.split(s) == custom_split(s)


def test_custom_split_whitespaces_mode_empty_string_limit_10():
    s = ""
    maxsplit = 10

    assert str.split(s, maxsplit=maxsplit) == custom_split(s, maxsplit=maxsplit)