"""
Module contains a custom context manager class for working with files.

Class:
    File
"""
import sys
import traceback


def eprint(*args, **kwargs):
    """Function to print in sys.stderr"""

    print(*args, file=sys.stderr, **kwargs)


class File:
    def __init__(self, filename, mode="r"):
        self.file = open(filename, mode)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        eprint(f"File descriptor was closed correctly!")
        if exc_type:
            eprint("Traceback:")
            traceback.print_tb(exc_tb)
            eprint(f"{exc_type.__name__} was thrown inside {File.__name__} context manager: {exc_val}!")
            return True


def main():
    with File("file.txt", "w") as file:
        file.write("Written from inside of custom context manager.").meme()


if __name__ == "__main__":
    main()
