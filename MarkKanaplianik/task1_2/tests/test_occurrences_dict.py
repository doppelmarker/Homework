from MarkKanaplianik.task1_2.occurrences_dict.occurrences_dict import get_occurrences_dict


def test_get_occurrences_positive01():
    string = "Oh, it is python"

    expected = {",": 1, " ": 3, "o": 2, "h": 2, "i": 2, "t": 2, "s": 1, "p": 1, "y": 1, "n": 1}

    actual = get_occurrences_dict(string)

    assert expected == actual


def test_get_occurrences_positive02():
    string = ""

    expected = {}

    actual = get_occurrences_dict(string)

    assert expected == actual


def test_get_occurrences_negative01():
    string = "1 2 3 4 5\n"

    expected = {"1": 1, " ": 3, "2": 1, "3": 1, "4": 1, "5": 1, "\n": 1}

    actual = get_occurrences_dict(string)

    assert expected != actual
