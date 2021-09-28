class NotEvenNumberError(Exception):
    """Raised if number is not even."""

    pass


class NumberNotGreaterThan2Error(Exception):
    """Raised if number is not greater than 2."""

    pass


def checker(num):
    if num % 2 != 0:
        raise NotEvenNumberError(f"{num} is not even!")
    elif num <= 2:
        raise NumberNotGreaterThan2Error(f"{num} is not greater than 2!")


def main():
    checker(10)
    checker(3)
    # checker(2)


if __name__ == "__main__":
    main()
