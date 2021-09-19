"""
### Task 4.4
Implement a function `split_by_index(s: str, indexes: List[int]) -> List[str]`
which splits the `s` string by indexes specified in `indexes`. Wrong indexes
must be ignored.
Examples:

>>> split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18])
['python', 'is', 'cool', ',', "isn't", 'it?']

>>> split_by_index("no luck", [42])
['no luck']
"""
from typing import List


def split_by_index(s: str, indexes: List[int]) -> List[str]:
    result = []
    current = 0
    for idx in indexes:
        if not type(idx) == int or idx < 0 or idx >= len(s):
            continue
        begin = current
        current = idx
        result.append(s[begin:current])
    result.append(s[current : len(s)])
    return result
