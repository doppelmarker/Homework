"""
Module contains endless fibonacci numbers generator.
"""


def endless_fib_generator():
    yield 1
    yield 1
    x, y = 1, 1
    while True:
        yield x + y
        x, y = y, x + y


def main():
    gen = endless_fib_generator()
    while True:
        print(next(gen))


if __name__ == "__main__":
    main()
