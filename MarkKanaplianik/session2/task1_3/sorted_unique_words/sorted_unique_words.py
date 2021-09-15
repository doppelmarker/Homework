"""
### Task 1.3
Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in sorted form.
Examples:
```
Input: ['red', 'white', 'black', 'red', 'green', 'black']
Output: ['black', 'green', 'red', 'white']
```
"""


def get_sorted_unique_words(sequence):
    return type(sequence)(sorted(set(sequence)))
