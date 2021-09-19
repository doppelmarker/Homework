"""
### Task 4.5
Implement a function `get_tuple(num: int) -> Tuple[int]` which returns a tuple
of a given integer's digits.
Example:
>>> get_tuple(87178291199)
(8, 7, 1, 7, 8, 2, 9, 1, 1, 9, 9)
"""
from typing import Tuple


def get_tuple(num: int) -> Tuple[int]:
    return tuple(map(lambda n: int(n), str(num)))
