"""
Module contains a custom iterator class, which accepts start and end of the interval as an init arguments and
gives only even numbers during iteration.

If user tries to iterate after it gave all possible numbers 'Out of numbers!' is printed.
"""


class EvenRange:
    def __init__(self, start, end):
        self.start = start if start % 2 == 0 else start + 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.start < self.end:
            next_value = self.start
            self.start += 2
            return next_value
        else:
            print("Out of numbers!")
            raise StopIteration


def main():
    er1 = EvenRange(7, 11)
    print(next(er1))
    print(next(er1))
    try:
        print(next(er1))
    except StopIteration:
        pass
    try:
        print(next(er1))
    except StopIteration:
        pass
    er2 = EvenRange(3, 14)
    for number in er2:
        print(number, end=" ")


if __name__ == "__main__":
    main()
