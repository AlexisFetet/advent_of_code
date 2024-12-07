"""
This file contains a code attempt for advent of code day 13
"""


import os
from typing import List


def find_sym_column(pattern):
    column = -1
    for indx in range(1, pattern.index("\n")):
        is_valid = True
        for line in pattern.split("\n"):
            if not (line[:indx].endswith(line[indx:][::-1])):
                is_valid = False
                break
        if is_valid:
            column = indx
            break
    return column


def part1(data: List[str]):
    columns = 0
    rows = 0
    for pattern in data:
        column = find_sym_column(pattern)
        if column != -1:
            columns += column
            continue
        pattern = "\n".join(["".join([line[k] for line in pattern.split("\n")]) for k in range(pattern.index("\n"))])
        row  = find_sym_column(pattern)
        if row != -1:
            rows += row
            continue
        pattern = "\n".join(["".join([line[k] for line in pattern.split("\n")][::-1]) for k in range(pattern.index("\n"))])
        column  = find_sym_column(pattern)
        if column != -1:
            columns += pattern.index("\n") - column
            continue
        pattern = "\n".join(["".join([line[k] for line in pattern.split("\n")][::-1]) for k in range(pattern.index("\n"))])
        row  = find_sym_column(pattern)
        if row != -1:
            rows += pattern.index("\n") - row
            continue
    return 100 * rows + columns

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().split("\n\n")

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().split("\n\n")

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {0}")
