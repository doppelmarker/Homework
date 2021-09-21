"""
### Task 5.2
Implement a function which search for most common words in the file.
Use `data/lorem_ipsum.txt` file as a example.

> NOTE: Remember about dots, commas, capital letters etc.

# >>> most_common_words('lorem_ipsum.txt')
['donec', 'etiam', 'aliquam']
"""

from collections import Counter
from pathlib import Path
from re import findall


def most_common_words(filepath, number_of_words=3):
    with open(filepath) as reader:
        pattern = r"\w+"
        words_collection = Counter(findall(pattern, reader.read()))
        return [word[0] for word in words_collection.most_common(number_of_words)]


if __name__ == "__main__":
    data_dir_path = Path(Path.cwd(), "../../..", "data")
    filename = "lorem_ipsum.txt"
    print(most_common_words(Path(data_dir_path, filename), 7))
