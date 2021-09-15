"""
Task 1.6
Write a Python program to print all unique values of all dictionaries in a list.
Examples:

Input: [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
Output: {'S005', 'S002', 'S007', 'S001', 'S009'}
"""
from functools import reduce


def merge_lists(l1, l2):
    return l1 + l2


def get_values(d):
    return list(d.values())


def get_unique_values_of_dicts(dicts):
    lists_of_values = list(map(get_values, dicts))
    return set(reduce(merge_lists, lists_of_values))
