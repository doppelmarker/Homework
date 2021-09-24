"""
Module provides a counter class.

Class:
    Counter
"""
from math import inf


class CounterMaximalValueReachedError(Exception):
    """Raised when maximal value of Counter is reached."""

    pass


class Counter:
    """Class to represent a counter.

    Methods
    -------
    increment:
        Increase current value of counter by 1
    get:
        Gets current value of counter
    """

    def __init__(self, *, start=0, stop=inf):
        if start > stop:
            raise ValueError(f"Start parameter '{start}' is greater than stop parameter '{stop}'.")
        self._current = start
        self.stop = stop

    def increment(self):
        self._current += 1
        if self._current > self.stop:
            self._current -= 1
            raise CounterMaximalValueReachedError(f"Maximal value {self.stop} is reached.")

    def get(self):
        return self._current


def main():
    c = Counter(start=42, stop=100)
    try:
        while True:
            c.increment()
            print(c.get())
    except CounterMaximalValueReachedError:
        pass
    print(c.get())

    c = Counter()
    c.increment()
    print(c.get())
    c.increment()
    print(c.get())

    c = Counter(start=42, stop=43)
    c.increment()
    print(c.get())

    try:
        c.increment()
    except CounterMaximalValueReachedError:
        pass
    print(c.get())

    Counter(start=50, stop=45)


if __name__ == "__main__":
    main()
