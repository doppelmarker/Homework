"""
### Task 1.4
Create a program that asks the user for a number and then prints out a list of all the [divisors](https://en.wikipedia.org/wiki/Divisor) of that number.
Examples:
```
Input: 60
Output: {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
```
"""


def find_all_divisors(n):
    return {num for num in range(n // 2, 0, -1) if n % num == 0} | {n}
