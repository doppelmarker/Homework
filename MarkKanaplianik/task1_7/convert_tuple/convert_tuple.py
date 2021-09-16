"""
### Task 1.7
Write a Python program to convert a given tuple of positive integers into an integer.
Examples:
```
Input: (1, 2, 3, 4)
Output: 1234
```
"""


from functools import reduce


def convert_tuple_to_integer(t):
    return int(reduce(lambda n1, n2: f"{n1}{n2}", t))
