"""
### Task 4.10
Implement a function that takes a number as an argument and returns a dictionary, where the key is a number and the value is the square of that number.
>>> generate_squares_recursion(5)
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
>>> generate_squares(5)
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
"""


def generate_squares_recursion(num):
    def insert_recursively(n, d):
        if n > 1:
            insert_recursively(n - 1, d)
        d[n] = n ** 2

    my_dict = dict()
    insert_recursively(num, my_dict)

    return my_dict


def generate_squares(num):
    return {n: n ** 2 for n in range(1, num + 1)}
