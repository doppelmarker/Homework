from MarkKanaplianik.task4_4.split_by_index.split_by_index import split_by_index


def test_split_by_index_normal_behaviour():
    s = "pythoniscool,isn'tit?"

    indexes = [6, 8, 12, 13, 18]

    expected = ["python", "is", "cool", ",", "isn't", "it?"]

    actual = split_by_index(s, indexes)

    assert expected == actual


def test_split_by_index_indexes_equal_or_bigger_than_length():
    s = "pythoniscool"

    indexes = [101, 12, 14, 3213, 23]

    expected = ["pythoniscool"]

    actual = split_by_index(s, indexes)

    assert expected == actual


def test_split_by_index_incorrect_indexes_types():
    s = "pythoniscool"

    indexes = [True, (), {}, []]

    expected = ["pythoniscool"]

    actual = split_by_index(s, indexes)

    assert expected == actual


def test_split_by_index_correct_and_incorrect_indexes_types():
    s = "pythoniscool"

    indexes = [True, 6, (), 8, {}, 12, []]

    expected = ["python", "is", "cool"]

    actual = split_by_index(s, indexes)

    assert expected == actual


def test_split_by_index_no_indexes():
    s = "pythoniscool"

    indexes = []

    expected = ["pythoniscool"]

    actual = split_by_index(s, indexes)

    assert expected == actual
