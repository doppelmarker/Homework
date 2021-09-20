"""
### Task 4.9
Implement a bunch of functions which receive a changeable number of strings and return next parameters:

1) characters that appear in all strings

2) characters that appear in at least one string

3) characters that appear at least in two strings

4) characters of alphabet, that were not used in any string

Note: use `string.ascii_lowercase` for list of alphabet letters

>>> test_strings = ["hello", "world", "python"]
>>> func_1_1(*test_strings)
{'o'}
>>> func_1_2(*test_strings).symmetric_difference({'d', 'e', 'h', 'l', 'n', 'o', 'p', 'r', 't', 'w', 'y'})
set()
>>> func_1_3(*test_strings).symmetric_difference({'h', 'l', 'o'})
set()
>>> func_1_4(*test_strings)
{'a', 'b', 'c', 'f', 'g', 'i', 'j', 'k', 'm', 'q', 's', 'u', 'v', 'x', 'z'}
"""
from functools import reduce


def func_1_1(*args):
    sorted_words = sorted(args, key=len)
    result = set()
    for char in sorted_words[0]:
        if not all(map(lambda s: char in s, sorted_words[1:])):
            continue
        result.add(char)
    return result


def func_1_2(*args):
    return set(reduce(set.union, (set(word) for word in args)))


def func_1_3(*args):
    characters = func_1_2(*args)
    result = set()
    for char in characters:
        counter = 0
        for word in args:
            if char in word:
                counter += 1
                if counter == 2:
                    result.add(char)
                    break
    return result
