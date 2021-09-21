import os
from pathlib import Path

import pytest

from MarkKanaplianik.task5_1.sort_names_file.sort_names_file import read_file, work


@pytest.fixture()
def data_dir_path():
    return Path(Path.cwd(), "../../..", "data")


@pytest.fixture()
def unsorted_names_file():
    return "unsorted_names.txt"


@pytest.fixture()
def sorted_names_file():
    return "sorted_names.txt"


@pytest.fixture()
def path_file_unsorted(data_dir_path, unsorted_names_file):
    return Path(data_dir_path, unsorted_names_file)


@pytest.fixture()
def path_file_sorted(data_dir_path, sorted_names_file):
    return Path(data_dir_path, sorted_names_file)


@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)


def test_sort_names_file_positive_01(change_test_dir, path_file_unsorted, path_file_sorted):
    work(path_file_unsorted, path_file_sorted)

    with open(path_file_unsorted) as reader_unsorted:
        with open(path_file_sorted) as reader_sorted:
            assert sorted(reader_unsorted) == reader_sorted
