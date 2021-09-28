import sys
from contextlib import contextmanager
from io import StringIO

import pytest

from MarkKanaplianik.task7_4.suppressor.custom_suppressor import Suppressor, suppressor


class Capturing:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self._value = self._stringio.getvalue()
        del self._stringio
        sys.stdout = self._stdout

    @property
    def value(self):
        return self._value


@contextmanager
def not_raises(exc):
    try:
        yield
    except exc:
        raise pytest.fail(f"DID RAISE {exc.__name__}")


def test_custom_suppressor_generator_suppressed_zero_division_error():
    with not_raises(ZeroDivisionError), suppressor(ZeroDivisionError):
        1 / 0


def test_custom_suppressor_class_suppressed_zero_division_error():
    with not_raises(ZeroDivisionError), Suppressor(ZeroDivisionError):
        1 / 0


def test_custom_suppressor_generator_exc_not_occurred():
    with Capturing() as captured_output, suppressor(ZeroDivisionError):
        1 + 0
    assert captured_output.value == f"Exception {ZeroDivisionError.__name__} hasn't occurred!\n"


def test_custom_suppressor_class_suppressed_exc_not_occurred():
    with Capturing() as captured_output, Suppressor(ZeroDivisionError):
        1 + 0
    assert captured_output.value == f"Exception {ZeroDivisionError.__name__} hasn't occurred!\n"
