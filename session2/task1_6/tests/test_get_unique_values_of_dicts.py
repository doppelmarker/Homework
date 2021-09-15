from session2.task1_6.print_unique_values_of_dicts.unique_values_of_dicts import (
    get_unique_values_of_dicts,
)


def test_unique_values_of_dicts_positive01():
    dicts = [
        {"V": "S001"},
        {"V": "S002"},
        {"VI": "S001"},
        {"VI": "S005"},
        {"VII": "S005"},
        {"V": "S009"},
        {"VIII": "S007"},
    ]

    expected = {"S001", "S005", "S009", "S002", "S007"}

    actual = get_unique_values_of_dicts(dicts)

    assert expected == actual
