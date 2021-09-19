from MarkKanaplianik.task4_2.check_palindrome.check_palindrome import is_palindrome


def test_is_palindrome_positive01():
    string = "1234321"

    expected = True

    actual = is_palindrome(string)

    assert expected == actual


def test_is_palindrome_negative01():
    string = "123"

    expected = True

    actual = is_palindrome(string)

    assert expected != actual
