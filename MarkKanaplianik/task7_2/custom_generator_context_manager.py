"""
Module contains a custom generator-based context manager for working with files.

Class:
    File
"""
import sys
from contextlib import contextmanager


def eprint(*args, **kwargs):
    """Function to print in sys.stderr"""

    print(*args, file=sys.stderr, **kwargs)


@contextmanager
def open_file(filename, mode="r"):
    file = open(filename, mode)
    try:
        yield file
    except Exception as e:
        eprint(
            f"{e.__class__.__name__} was thrown inside {sys._getframe().f_code.co_name} context manager: {e.args[0]}!"
        )
    finally:
        file.close()
        eprint(f"File descriptor was closed correctly!")


def main():
    with open_file("file.txt", "w") as file:
        file.write("Written from inside of custom context manager.").meme()


if __name__ == "__main__":
    main()
