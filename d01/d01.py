"""
This file contains a code attempt for advent of code day 1
"""


import os


def solve(line, part=1):
    floor = 0
    step_number = 0
    for step in line:
        if '(' == step:
            floor += 1
            step_number += 1
        elif ')' == step:
            floor -= 1
            step_number += 1
            if 2 == part and -1 == floor:
                break
        else:
            raise ValueError
    return floor if 1 == part else step_number


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {solve(my_input[0], part=1)}")
    print(f"Answer part2 : {solve(my_input[0], part=2)}")
