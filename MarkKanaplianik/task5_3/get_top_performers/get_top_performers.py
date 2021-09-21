"""### Task 5.3 File `data/students.csv` stores information about students in [CSV]
(https://en.wikipedia.org/wiki/Comma-separated_values) format.
This file contains the student’s names, age and average mark.

1) Implement a function which receives file path and returns names of top performer students

>>> data_dir_path = Path(Path.cwd(), "../../..", "data")
>>> filename = "students.csv"
>>> filepath = Path(data_dir_path, filename)
>>> get_top_performers(filepath, 5)
['Teresa Jones', 'Richard Snider', 'Jessica Dubose', 'Heather Garcia', 'Joseph Head']

2) Implement a function which receives the file path with students info and writes CSV student information to the new
file in descending order of age.

Result:
student name,age,average mark
Verdell Crawford,30,8.86
Brenda Silva,30,7.53
...
Lindsay Cummings,18,6.88
Raymond Soileau,18,7.27
"""
import csv
from pathlib import Path


def get_top_performers(filepath, number_of_students=3):
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        sorted_students = sorted(reader, key=lambda student: student[2], reverse=True)[1 : number_of_students + 1]
        return [student[0] for student in sorted_students]


def write_to_csv_age_descending(filepath):
    with open(filepath, "r") as file_to_read:
        with open(Path(filepath.parent, f"sorted_{Path(filepath).name}"), "w", newline="") as file_to_write:
            reader = csv.reader(file_to_read)
            writer = csv.writer(file_to_write)

            writer.writerow(next(reader))

            sorted_students = sorted(reader, key=lambda student: student[1], reverse=True)
            writer.writerows(sorted_students)


def main():
    path_dir_data = Path(Path.cwd(), "../../..", "data")
    name_file_students = "students.csv"
    path_file_students = Path(path_dir_data, name_file_students)

    print(get_top_performers(path_file_students, 5))
    write_to_csv_age_descending(path_file_students)


if __name__ == "__main__":
    main()
