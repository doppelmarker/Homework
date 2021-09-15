"""
Task 1.1
Write a Python program to calculate the length of a string without using the `len` function.
"""


def count_str_length(s):
    return sum(map(lambda _: 1, s))
