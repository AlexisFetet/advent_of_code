"""
This file contains a code attempt for advent of code day 9
"""

import re
import os


def part1(lines):
    lines = [[int(x) for x in re.findall(r"(-?(?:\d)+)",line)] for line in lines]
    values = []
    for line in lines:
        steps = [line]
        while any(steps[-1]):
            steps.append(
                list(map(lambda x: x[1]-x[0], list(zip(steps[-1][:-1], steps[-1][1:])))))
        score = 0
        for elem in steps[::-1]:
            score += elem[-1]
        values.append(score)
    return sum(values)

def part2(lines):
    lines = [[int(x) for x in re.findall(r"(-?(?:\d)+)",line)] for line in lines]
    values = []
    for line in lines:
        steps = [line]
        while any(steps[-1]):
            steps.append(
                list(map(lambda x: x[1]-x[0], list(zip(steps[-1][:-1], steps[-1][1:])))))
        score = 0
        for elem in steps[::-1]:
            score = elem[0] - score
        values.append(score)
    return sum(values)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
