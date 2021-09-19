"""
### Task 4.3
Implement a function which works the same as `str.split` method
(without using `str.split` itself, of course).
"""


def custom_split(s: str, sep=None, maxsplit=-1):
    if sep is None:
        def split_whitespaces():
            result = []
            _s = s.lstrip()
            current = 0
            while current < len(_s):
                if len(result) == maxsplit:
                    part = _s[current:len(_s)].lstrip()
                    if bool(part):
                        result.append(part)
                    return result
                while current < len(_s) and _s[current] == " ":
                    current += 1
                begin = current
                while current < len(_s) and _s[current] != " ":
                    current += 1
                part = _s[begin:current]
                if bool(part):
                    result.append(part)
                current += 1
            return result
        split_func = split_whitespaces
    else:
        def split_normal():
            result = []
            current = 0
            while current < len(s) + 1:
                if len(result) == maxsplit:
                    result.append(s[current:len(s)])
                    return result
                begin = current
                while current < len(s) and s[current] != sep:
                    current += 1
                result.append(s[begin:current])
                current += 1
            return result
        split_func = split_normal
    return split_func()


print(custom_split(" 1   2 3       4  ", " "))
# print(custom_split("   1   2   3       4  "))
# print(str.split("   1   2   3       4  "))
print(str.split(" 1   2 3       4  ", " "))
