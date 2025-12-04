"""
This file contains a code attempt for advent of code day 2
"""

import math
import os

def solve_px(line:str, maxi_repeat = None):
    ranges = [(int(range_.split('-')[0]), int(range_.split('-')[1])) for range_ in line.split(',')]
    count = 0
    for minimum, maximum in ranges:
        invalids = set()
        digits_min = int(math.log10(minimum)) + 1
        digits_max = int(math.log10(maximum)) + 1
        repeating_min = 2
        repeating_max = digits_max if maxi_repeat is None else maxi_repeat
        for repeating in range(repeating_min, repeating_max + 1):
            power_10 = math.ceil(digits_min / repeating)
            increment = 1
            for _ in range(1, repeating):
                increment *= 10 ** power_10
                increment += 1
            for test in range(minimum - (minimum % increment), maximum + 1, increment):
                if test <= 1:
                    continue
                digits_test = int(math.log10(test)) + 1
                if digits_test % repeating != 0:
                    continue
                if minimum <= test:
                    invalids.add(test)
        count += sum(invalids)
    return count

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read()

    print(f"Answer exemple part1 : {solve_px(my_tests, 2)}")
    print(f"Answer part1 : {solve_px(my_input, 2)}")
    print(f"Answer exemple part2 : {solve_px(my_tests)}")
    print(f"Answer part2 : {solve_px(my_input)}")
