"""
This file contains a code attempt for advent of code day 8
"""

import re
import os

from math import lcm


def solve(lines, part):
    path = lines[0].replace('L', '0').replace('R', '1')
    nodes = {elem[0]: (elem[1], elem[2]) for elem in [
        re.findall(r"(\w+)", line) for line in lines[2:]]}
    path_indx = 0
    count = 0
    if part == 1:
        starts = ["AAA"]
    else:
        starts = [elem for elem in nodes.keys() if elem[2] == 'A']
    cycles = []
    for target in starts:
        path_indx = 0
        count = 0
        current = target
        while (current[2] != 'Z'):
            count += 1
            current = nodes[current][int(path[path_indx])]
            path_indx = (path_indx + 1) % len(path)
        cycles.append(count)
    return lcm(*cycles)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {solve(my_input, 1)}")
    print(f"Answer part2 : {solve(my_input, 2)}")
