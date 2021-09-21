from pathlib import Path
from typing import List, TextIO


def read_file(reader: TextIO):
    return (line for line in reader)


def write_file(writer: TextIO, lines: List[str]):
    for line in lines:
        writer.write(line)


def work(path_file_read: Path, path_file_write: Path):
    with open(path_file_read) as reader:
        lines = list(read_file(reader))

    lines.sort()

    with open(path_file_write, "w") as writer:
        write_file(writer, lines)


test_dir = Path(Path.cwd(), "../../..", "data")
name_file_read = "unsorted_names.txt"
path_file_read = Path(test_dir, name_file_read)
name_file_write = "sorted_names.txt"
path_file_write = Path(test_dir, name_file_write)
work(path_file_read, path_file_write)
