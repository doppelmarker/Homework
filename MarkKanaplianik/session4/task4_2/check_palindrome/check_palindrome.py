"""
### Task 4.2
Write a function that check whether a string is a palindrome or not. Usage of
any reversing functions is prohibited. To check your implementation you can use
strings from [here](https://en.wikipedia.org/wiki/Palindrome#Famous_palindromes).
"""


def is_palindrome(s: str):
    for idx in range(0, len(s) // 2):
        if s[idx] != s[-idx - 1]:
            return False
    return True
