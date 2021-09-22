"""
This module provides a function-based decorator to remember the last result of function it decorates.

Function:
    remember_result
"""
import functools
from typing import Union


def remember_result(f):
    """Remember last result of function it decorates and print it before next call."""
    prev_result = None

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal prev_result
        print(f"Last result = '{prev_result}'")
        result = f(*args, **kwargs)
        prev_result = result

    return wrapper


def sum_list(*args: Union[int, str]) -> str:
    """Concatenate int and str arguments passed.

    Print final result in the format: Result = <result>.
    If a sequence of int arguments takes place, this concatenates the sum of this sequence to the intermediate result.

    Parameters
    ----------
    *args: Union[int, str]
        Arguments to be concatenated

    Raises
    ------
    ValueError
        If neither int nor str argument was passed

    Examples
    --------
    Concatenate strings.

    >>> sum_list("a", "b", "c")
    Result = 'abc'
    'abc'

    Sum sequences of integer values and concatenate with other strings.

    >>> sum_list(1, 2, "f", 123, 3, "d", 5)
    Result = '3f126d5'
    '3f126d5'
    """

    result = ""
    i = 0
    while i < len(args):
        if isinstance(args[i], str):
            result += args[i]
            i += 1
        elif isinstance(args[i], int):
            int_sum = 0
            while i < len(args) and isinstance(checked_arg := args[i], int):
                i += 1
                int_sum += checked_arg
            result += str(int_sum) if bool(int_sum) else ""
        else:
            raise ValueError("Function accepts only str and int arguments.")

    print(f"Result = '{result}'")
    return result


def main():
    decorated_sum_list = remember_result(sum_list)

    decorated_sum_list("a", "b", "c")
    decorated_sum_list("d", "e", "f")
    decorated_sum_list("a")
    decorated_sum_list(1, 2, "f", 123, 4, 5)


if __name__ == "__main__":
    main()
