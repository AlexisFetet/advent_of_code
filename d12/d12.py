"""
This file contains a code attempt for advent of code day 12
"""

from functools import lru_cache
from itertools import product
import re
import os

DIGIT = re.compile(r"(\d+)")

@lru_cache(maxsize=None)
def get(needed, needed_sharp):
    return [elem for elem in product('.#', repeat=needed) if elem.count('#') == needed_sharp]

def key(line):
    return [len(string) for string in re.findall(r"(#+)", line)]


def part1(lines: list[str]):
    targets = [[int(digit) for digit in DIGIT.findall(line)] for line in lines]
    counter = 0
    for line, target in zip(lines, targets):
        needed = line.count('?')
        needed_sharp = sum(target) - line.count('#')
        all_combinations = get(needed, needed_sharp)
        init_str = line.split()[0]
        for combination in all_combinations:
            working_str = ''
            replaced = 0
            for char in init_str:
                if char != '?':
                    working_str += char
                else:
                    working_str += combination[replaced]
                    replaced += 1
            if key(working_str) == target:
                counter += 1
    return counter

def part2(lines: list[str]):
    

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    import time
    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_tests)}")
