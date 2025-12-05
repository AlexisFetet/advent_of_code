"""
This file contains a code attempt for advent of code day 5
"""


import os

def solve_p1(ranges, produce):
    ranges = [list(map(int, elem.split("-"))) for elem in ranges]
    produce = list(map(int, produce))
    counter = 0
    for product in produce:
        for range_ in ranges:
            if (range_[0] <= product <= range_[1]):
                counter += 1
                break
    return counter

def merge(ranges):
    actual_ranges = []
    for range_ in ranges:
        intersect = False
        contained = False
        for actual_range_ in actual_ranges:
            replace_min = False
            replace_max = False
            if actual_range_[0] <= range_[0] <= range_[1] <= actual_range_[1]:
                contained = True
                break
            if range_[0] <= actual_range_[1] <= range_[1]:
                replace_max = True
                intersect = True
            if range_[0] <= actual_range_[0] <= range_[1]:
                replace_min = True
                intersect = True
            if replace_min:
                actual_range_[0] = range_[0]
            if replace_max:
                actual_range_[1] = range_[1]
        if contained:
            continue
        if not intersect:
            actual_ranges.append(range_)
    return actual_ranges

def solve_p2(ranges):
    ranges = [list(map(int, elem.split("-"))) for elem in ranges]
    actual_ranges = merge(ranges)
    while ranges != actual_ranges:
        ranges = actual_ranges
        actual_ranges = merge(ranges)
    return sum(map(lambda x: x[1]-x[0]+1, actual_ranges))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()
    
    my_tests_sep = my_tests.index("")
    my_input_sep = my_input.index("")

    print(f"Answer exemple part1 : {solve_p1(my_tests[:my_tests_sep], my_tests[my_tests_sep+1:])}")
    print(f"Answer part1 : {solve_p1(my_input[:my_input_sep], my_input[my_input_sep+1:])}")
    print(f"Answer exemple part1 : {solve_p2(my_tests[:my_tests_sep])}")
    print(f"Answer part2 : {solve_p2(my_input[:my_input_sep])}")
