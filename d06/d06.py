"""
This file contains a code attempt for advent of code day 6
"""

import re
import os
import math as ma

NUMBER_REGEX = re.compile(r"([0-9]+)")


def solve(time, distance):
    sqrt = ma.sqrt(time ** 2 - 4 * distance)
    return ((time - sqrt)/2, (time + sqrt)/2)


def part1(lines):
    times = map(int, NUMBER_REGEX.findall(lines[0]))
    distances = map(int, NUMBER_REGEX.findall(lines[1]))
    prod = 1
    for time, distance in zip(times, distances):
        inf_val, upper_val = solve(time, distance)
        inf_val = int(inf_val) + 1
        upper_val = int(upper_val - 1)
        solutions = upper_val - inf_val + 1
        prod *= solutions
    return prod


def part2(lines):
    time = int(NUMBER_REGEX.findall(lines[0].replace(' ', ''))[0])
    distance = int(NUMBER_REGEX.findall(lines[1].replace(' ', ''))[0])
    inf_val, upper_val = solve(time, distance)
    inf_val = int(inf_val) + 1
    upper_val = int(upper_val) if int(
        upper_val) != upper_val else int(upper_val) - 1
    solutions = upper_val - inf_val + 1
    return solutions


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
