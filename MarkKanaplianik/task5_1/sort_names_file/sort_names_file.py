"""### Task 4.1
Open file `data/unsorted_names.txt` in data folder.
Sort the names and write them to a new file called `sorted_names.txt`.
Each name should start with a new line as in the following example:

Adele
Adrienne
...
Willodean
Xavier
"""

from pathlib import Path
from typing import TextIO


def read_file(reader: TextIO):
    return (line for line in reader)


def work(path_file_read: Path, path_file_write: Path):
    with open(path_file_read) as reader:
        with open(path_file_write, "w") as writer:
            writer.writelines(sorted(reader))
