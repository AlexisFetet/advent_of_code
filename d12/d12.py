"""
This file contains a code attempt for advent of code day 12
"""

from functools import lru_cache
from itertools import product
import re
import os

DIGIT = re.compile(r"(\d+)")


@lru_cache(maxsize=None)
def recursive(string, target):
    if string == '':
        return 1 if not target else 0
    if not target:
        return 1 if '#' not in string else 0

    arrangements = 0
    if string[0] in '.?':
        arrangements += recursive(string[1:], target)
    if string[0] in '#?':
        if (target[0] <= len(string) and "." not in string[: target[0]]
                and (target[0] == len(string) or string[target[0]] != "#")):
            arrangements += recursive(string[target[0] + 1:], target[1:])
    return arrangements


def part1(lines: list[str]):
    data = [line.split() for line in lines]
    data = [(elem[0], tuple(int(x) for x in elem[1].split(','))) for elem in data]
    return sum([recursive(string, target) for string, target in data])


def part2(lines: list[str]):
    data = [line.split() for line in lines]
    data = [(elem[0], tuple(int(x) for x in elem[1].split(','))) for elem in data]
    return sum([recursive('?'.join([string] * 5), target * 5) for string, target in data])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    import time
    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
