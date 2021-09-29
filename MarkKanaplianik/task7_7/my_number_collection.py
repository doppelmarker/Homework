"""
Module contains a custom collection class, which is able to contain only numbers.
"""
import types
from functools import wraps
from numbers import Number
from typing import Iterable


class Validator:
    @staticmethod
    def validate_init(f):
        @wraps(f)
        def wrapper(self, *args):
            args_amount = len(args)
            if args_amount == 1:
                if isinstance(args[0], types.GeneratorType):
                    # generator functions are forbidden as well because they are not iterable
                    raise TypeError("Generator expression was passed to init!")
                if not isinstance(args[0], Iterable):
                    raise TypeError("Not Iterable was passed to init!")
                if isinstance(args[0], str):
                    raise TypeError("String was passed to init!")
                for e in args[0]:
                    if not isinstance(e, Number):
                        raise TypeError(f"MyNumberCollection supports only numbers, {e!r} of type {type(e)} was given!")
            elif args_amount == 3:
                if not isinstance(args[0], int):
                    raise ValueError(f"Start parameter must be integer, got type {type(args[0])} instead!")
                elif not isinstance(args[1], int):
                    raise ValueError(f"Stop parameter must be integer, got type {type(args[1])} instead!")
                elif not isinstance(args[2], int):
                    raise ValueError(f"Step parameter must be integer, got type {type(args[2])} instead!")
                elif args[0] > args[1]:
                    raise ValueError(f"Start parameter must be less or equal to end parameter!")
            else:
                raise ValueError(f"Init expected either 1 or 3 arguments, got {args_amount} instead!")
            f(self, *args)

        return wrapper

    @staticmethod
    def validate_append(f):
        @wraps(f)
        def wrapper(self, e):
            if not isinstance(e, Number):
                raise TypeError(f"{e!r} object is not a number!")
            f(self, e)

        return wrapper


class CustomCollectionIndexError(IndexError):
    pass


class MyNumberCollection:
    @Validator.validate_init
    def __init__(self, *args):
        if len(args) == 1:
            self._collection = list(args[0])
        else:
            self._collection = [i for i in range(args[0], args[1], args[2])]
            self._collection.append(args[1])

    @Validator.validate_append
    def append(self, e):
        self._collection.append(e)

    def __add__(self, other: "MyNumberCollection"):
        return MyNumberCollection(self._collection + other._collection)

    def __getitem__(self, item):
        try:
            return self._collection[item] ** 2
        except (IndexError, TypeError) as e:
            raise CustomCollectionIndexError(f"Invalid index: {item!r}!") from e

    def __iter__(self):
        return iter(self._collection)

    def __str__(self):
        return f"{self._collection}"

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._collection)


def main():
    col1 = MyNumberCollection(0, 5, 2)
    print(col1)

    col2 = MyNumberCollection((1, 2, 3, 4, 5))
    print(col2)

    try:
        col3 = MyNumberCollection((1, 2, 3, "4", 5))
    except TypeError as e:
        print(e)

    col1.append(7)
    print(col1)

    try:
        col2.append("string")
    except TypeError as e:
        print(e)

    print(col1 + col2)
    print(col1)
    print(col2)
    print(col2[4])

    for item in col1:
        print(item, end=" ")

    print("\n" + repr(col1))


if __name__ == "__main__":
    main()
