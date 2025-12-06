"""
This file contains a code attempt for advent of code day 6
"""

from functools import reduce
import itertools
import os

def number_getter_p1(lines, minimum, maximum):
    return [int(line[minimum+1:maximum]) for line in lines[:-1]]

def number_getter_p2(lines, minimum, maximum):
    numbers = ["" for _ in range(minimum+1, maximum if maximum is not None else len(lines[0]))]
    for line in lines[:-1]:
        for index, char in enumerate(line[minimum+1:maximum]):
            numbers[index] += char
    return list(map(int, numbers))

def solve_px(lines, number_getter):
    spaces = [set([index for index, element in enumerate(line) if element == ' ']) for line in lines]
    common_spaces = list(set.intersection(*spaces)) + [-1]
    common_spaces.sort()
    common_spaces += [None]
    counter = 0
    for minimum, maximum in itertools.pairwise(common_spaces):
        numbers = number_getter(lines, minimum, maximum)
        operator = lines[-1][minimum+1:maximum].strip()
        counter += reduce((lambda x, y: x + y) if operator == '+' else (lambda x, y: x * y), numbers)
    return counter


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {solve_px(my_tests, number_getter_p1)}")
    print(f"Answer part1 : {solve_px(my_input, number_getter_p1)}")
    print(f"Answer exemple part2 : {solve_px(my_tests, number_getter_p2)}")
    print(f"Answer part2 : {solve_px(my_input, number_getter_p2)}")
