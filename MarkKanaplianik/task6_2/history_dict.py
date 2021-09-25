"""
Module provides HistoryDict class, which memorizes 10 latest changed keys.

Class:
    HistoryDict
"""
from collections import deque


class HistoryDict(dict):
    """Class, which derives from dict.

    Instances have _history attribute which stores 10 latest changed keys.
    """

    def __new__(cls, *args, **kwargs):
        new_instance = super(HistoryDict, cls).__new__(cls)
        new_instance._history = deque(maxlen=10)
        return new_instance

    def set_value(self, key, value):
        self[key] = value
        self._history.appendleft(key)

    def get_history(self):
        return list(self._history)


def main():
    hd = HistoryDict({"1": 1})

    for i in range(10):
        hd.set_value("foo", "bar")
    for i in range(5):
        hd.set_value("fizz", "buzz")

    print(hd)
    print(hd.get_history())


if __name__ == "__main__":
    main()
