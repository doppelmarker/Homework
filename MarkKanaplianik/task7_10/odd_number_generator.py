"""
Module contains endless generator of odd numbers.
"""


def endless_generator():
    start = 1
    while True:
        yield start
        start += 2


def main():
    gen = endless_generator()
    while True:
        print(next(gen))


if __name__ == "__main__":
    main()
