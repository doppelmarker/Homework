def is_palindrome(s: str):
    for idx in range(0, len(s) // 2):
        if s[idx] != s[-idx - 1]:
            return False
    return True
