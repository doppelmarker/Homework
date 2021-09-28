"""
Module contains custom decorator with context manager support based on ContextDecorator from contextlib.
"""
import time
from contextlib import ContextDecorator


class ExecutionTimeContextDecorator(ContextDecorator):
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open("log.txt", "w") as file:
            file.write(str(time.time() - self.start))


@ExecutionTimeContextDecorator()
def sample_function():
    for i in range(5):
        time.sleep(1)


def main():
    sample_function()


if __name__ == "__main__":
    main()
