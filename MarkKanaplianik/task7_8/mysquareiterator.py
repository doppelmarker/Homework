"""
Module contains a custom iterator class which gives squares of elements of collection it iterates through.
"""


class MySquareIterator:
    def __init__(self, collection):
        self._collection = collection

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < len(self._collection):
            next_value = self._collection[self._i] ** 2
            self._i += 1
            return next_value
        else:
            raise StopIteration


def main():
    lst = [1, 2, 3, 4, 5]
    itr = MySquareIterator(lst)
    for item in itr:
        print(item, end=" ")


if __name__ == "__main__":
    main()
