"""
### Task 5.2
Implement a function which search for most common words in the file.
Use `data/lorem_ipsum.txt` file as a example.

> NOTE: Remember about dots, commas, capital letters etc.

>>> data_dir_path = Path(Path.cwd(), "../../..", "data")
>>> filename = "lorem_ipsum.txt"
>>> filepath = Path(data_dir_path, filename)
>>> most_common_words(filepath)
['donec', 'etiam', 'aliquam']
>>> most_common_words(filepath, 5)
['donec', 'etiam', 'aliquam', 'aenean', 'maecenas']
"""

from collections import Counter
from pathlib import Path
from re import findall


def most_common_words(filepath, number_of_words=3):
    with open(filepath) as reader:
        pattern = r"\w+"
        words_collection = Counter(findall(pattern, reader.read()))
        return [word[0] for word in words_collection.most_common(number_of_words)]
