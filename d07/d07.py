"""
This file contains a code attempt for advent of code day 7
"""

from copy import deepcopy
import os

def solve_px(lines):
    beams = [0] * len(lines[0])
    beams[lines[0].index('S')] = 1
    counter = 0
    for line in lines[1:]:
        new_beams = deepcopy(beams)
        if '^' not in line:
            continue
        for index, char in enumerate(line):
            if char == '^':
                if beams[index] != 0:
                    counter += 1
                    new_beams[index - 1] += beams[index]
                    new_beams[index] = 0
                    new_beams[index + 1] += beams[index]
        beams = new_beams
    return (counter, sum(beams))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple (part1, part2) : {solve_px(my_tests)}")
    print(f"Answer (part1, part2) : {solve_px(my_input)}")
