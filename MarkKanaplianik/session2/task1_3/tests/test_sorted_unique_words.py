from MarkKanaplianik.session2.task1_3.sorted_unique_words.sorted_unique_words import (
    get_sorted_unique_words,
)


def test_sorted_unique_words_positive01():
    sequence = ["red", "white", "black", "red", "green", "black"]

    expected = ["black", "green", "red", "white"]

    actual = get_sorted_unique_words(sequence)

    assert expected == actual


def test_sorted_unique_words_positive02():
    sequence = ("red", "white", "black", "red", "green", "black")

    expected = ("black", "green", "red", "white")

    actual = get_sorted_unique_words(sequence)

    assert expected == actual


def test_sorted_unique_words_incorrect_sequence_type():
    sequence = ["red", "white", "black", "red", "green", "black"]

    expected = ("black", "green", "red", "white")

    actual = get_sorted_unique_words(sequence)

    assert expected != actual
