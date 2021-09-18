"""
### Task 4.1
Implement a function which receives a string and replaces all `"` symbols
with `'` and vise versa.
"""


def replace_quotes(s: str, old_quotes="'"):
    if old_quotes != "'" and old_quotes != '"':
        raise ValueError(f"Expected quotes symbols (\" or '). Got {old_quotes} instead.")

    new_quotes = '"' if old_quotes == "'" else "'"

    return s.replace(old_quotes, new_quotes)
