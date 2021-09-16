from MarkKanaplianik.task1_5.sort_dict_by_key.sort_dict_by_key import sort_dict_by_key


def test_sort_dict_by_key_positive01():
    d = {1: "1", 0: "0", 2: "2", 5: "5", 4: "4"}

    expected = {0: "0", 1: "1", 2: "2", 4: "4", 5: "5"}

    actual = sort_dict_by_key(d)

    assert expected == actual
