"""
### Task 4.8
Implement a function `get_pairs(lst: List) -> List[Tuple]` which returns a list
of tuples containing pairs of elements. Pairs should be formed as in the
example. If there is only one element in the list return `None` instead.
Example:
>>> get_pairs([1, 2, 3, 8, 9])
[(1, 2), (2, 3), (3, 8), (8, 9)]

>>> get_pairs(['need', 'to', 'sleep', 'more'])
[('need', 'to'), ('to', 'sleep'), ('sleep', 'more')]

>>> get_pairs([1]) is None
True
"""
from typing import List, Tuple


def get_pairs(lst: List) -> List[Tuple]:
    if len(lst) == 1:
        return
    return list(zip(lst, lst[1:]))
