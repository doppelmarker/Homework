"""
### Task 4.9
Implement a bunch of functions which receive a changeable number of strings and return next parameters:

1) characters that appear in all strings

2) characters that appear in at least one string

3) characters that appear at least in two strings

4) characters of alphabet, that were not used in any string

Note: use `string.ascii_lowercase` for list of alphabet letters

# >>> test_strings = ["hello", "world", "python", ]
# >>> func_1_1(*test_strings)
{'o'}
# >>> test_1_2(*test_strings)
{'d', 'e', 'h', 'l', 'n', 'o', 'p', 'r', 't', 'w', 'y'}
# >>> test_1_3(*test_strings)
{'h', 'l', 'o'}
# >>> test_1_4(*test_strings)
{'a', 'b', 'c', 'f', 'g', 'i', 'j', 'k', 'm', 'q', 's', 'u', 'v', 'x', 'z'}
"""


def func_1_1(*args):
    sorted_words = sorted(args, key=len)
    result = set()
    for char in sorted_words[0]:
        if not all(map(lambda s: char in s, sorted_words[1:])):
            continue
        result.add(char)
    return result


words = [
    "hello",
    "worldl",
    "pythonl",
]
print(func_1_1(*words))
