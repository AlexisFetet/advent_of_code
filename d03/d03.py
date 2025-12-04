"""
This file contains a code attempt for advent of code day 3
"""

import math
import os

def solve_px(bank, cell_count):
    values = [int(cell) for cell in bank]
    if cell_count == 1:
        return max(values)
    inx = values.index(max(values[:-(cell_count-1)]))
    smaller = solve_px(values[(inx+1):], cell_count-1)
    digits = int(math.log10(smaller)) + 1
    return values[inx] * (10 ** digits) + smaller

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {sum(map(lambda elem: solve_px(elem, 2), my_tests))}")
    print(f"Answer part1 : {sum(map(lambda elem: solve_px(elem, 2), my_input))}")
    print(f"Answer exemple part2 : {sum(map(lambda elem: solve_px(elem, 12), my_tests))}")
    print(f"Answer part2 : {sum(map(lambda elem: solve_px(elem, 12), my_input))}")
