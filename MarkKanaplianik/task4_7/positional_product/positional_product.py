"""
### Task 4.7
Implement a function `foo(List[int]) -> List[int]` which, given a list of
integers, return a new list such that each element at index `i` of the new list
is the product of all the numbers in the original array except the one at `i`.
Example:
>>> foo([1, 2, 3, 4, 5])
[120, 60, 40, 30, 24]

>>> foo([3, 2, 1])
[2, 3, 6]
"""
from typing import List


def foo(numbers: List[int]) -> List[int]:
    result = []
    for i in range(len(numbers)):
        product = 1
        for j, number in enumerate(numbers):
            if i != j:
                product *= number
        result.append(product)
    return result
