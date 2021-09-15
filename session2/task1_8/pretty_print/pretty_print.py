"""
### Task 1.8
Write a program which makes a pretty print of a part of the multiplication table.
Examples:
```
Input:
a = 2
b = 4
c = 3
d = 7

Output:
	3	4	5	6	7
2	6	8	10	12	14
3	9	12	15	18	21
4	12	16	20	24	28
```
"""


def print_multiplication_table(a, b, c, d):
    print(f"{'':7}", end="")
    for i in range(c, d + 1):
        print(f"{i:7}", end="")
    print("\n")

    for row_idx, row_val in enumerate(range(a, b + 1)):
        for col_idx, col_val in enumerate(range(c, d + 1)):
            if col_idx == 0:
                print(f"{range(a, b + 1)[row_idx]:7}", end="")
            print(f"{row_val * col_val:7}", end="")
        print("\n")
