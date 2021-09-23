"""
Module provides a function-based decorator to remember the first result of the function it decorates.

Function:
    call_once
"""
from functools import wraps
from typing import Union


def call_once(f):
    """Remember the first result of function it decorates.

    Whenever the function is repeatedly called the decorator returns the result of the first call instead of calling
    the decorated function.

    Parameters
    ----------
    f:
        Decorated function
    """
    cache = None

    @wraps(f)
    def wrapper(*args):
        nonlocal cache
        if cache:
            return cache
        cache = result = f(*args)
        return result

    return wrapper


@call_once
def sum_of_numbers(*numbers: Union[int, float]) -> int:
    """Sum numbers."""
    return sum(numbers)


def main():
    """Run task."""
    # Нет варнинга при передаче аргументов, не являющихся int или float, хотя, как я считаю, должен быть, ведь wraps
    # скопировал аннотации функции sum_of_numbers во wrapper. Пример: sum_of_numbers("", 1, "", 1.12)
    print(sum_of_numbers(1, 2, 3, 4, 5))
    print(sum_of_numbers(1, 2, 3))
    print(sum_of_numbers(1, 2))


if __name__ == "__main__":
    main()
