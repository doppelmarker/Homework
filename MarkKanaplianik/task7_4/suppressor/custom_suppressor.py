"""
Module provides custom exception suppressor implemented both as generator and class.
"""
from contextlib import contextmanager


@contextmanager
def suppressor(exc):
    try:
        yield
    except exc:
        pass
    else:
        print(f"Exception {exc.__name__} hasn't occurred!")


class Suppressor:
    def __init__(self, exc):
        self.exc = exc

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.exc is exc_type:
            return True
        else:
            print(f"Exception {self.exc.__name__} hasn't occurred!")
