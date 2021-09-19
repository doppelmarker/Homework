import pytest

from MarkKanaplianik.task4_1.replace_quotes.replace_quotes import replace_quotes


def test_replace_quotes_single_to_double():
    string = "a'b'c'd'e'f"

    expected = 'a"b"c"d"e"f'

    actual = replace_quotes(string)

    assert expected == actual


def test_replace_quotes_double_to_single():
    string = 'a"b"c"d"e"f'

    expected = "a'b'c'd'e'f"

    actual = replace_quotes(string, '"')

    assert expected == actual


def test_replace_quotes_incorrect_old_quotes_argument_value_error():
    string = "a'b'c'd'e'f"

    with pytest.raises(ValueError):
        replace_quotes(string, "")
