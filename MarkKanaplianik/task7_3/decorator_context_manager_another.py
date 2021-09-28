"""
Module provides another way to define a decorator with context manager support.
"""
import time


class Decontext(object):
    """Makes a context manager act also as decorator."""

    def __init__(self, context_manager):
        self._cm = context_manager

    def __enter__(self):
        return self._cm.__enter__()

    def __exit__(self, *args, **kwargs):
        return self._cm.__exit__(*args, **kwargs)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper


class ExecutionTimeContextManager:
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open("log.txt", "w") as file:
            file.write(str(time.time() - self.start))


@Decontext(ExecutionTimeContextManager())
def sample_function():
    for i in range(5):
        time.sleep(1)


def main():
    sample_function()


if __name__ == "__main__":
    main()
