"""
This file contains a code attempt for advent of code day 18
"""

from itertools import pairwise
from numpy import angle
import matplotlib.pyplot as plt
import re
import os

STEP_REGEX = re.compile(r"([RLUD]) ([0-9]+) \(#([0-9a-f]+)\)")

dirs = {
    '0': 1,   'R': 1,
    '1': -1j, 'D': -1j,
    '2': -1,  'L': -1,
    '3': 1j,  'U': 1j,
}

def solve(steps):
    offset = (dirs[steps[-1][0]] + dirs[steps[0][0]]) * 0.5j
    current = 0
    points = [current + offset]
    for step_a, step_b in pairwise(steps):
        offset = (dirs[step_a[0]] + dirs[step_b[0]]) * 0.5j
        current += dirs[step_a[0]] * step_a[1]
        points.append(current + offset)
    area = (points[-1].imag + points[0].imag)*(points[-1].real - points[0].real)
    for point_a, point_b in pairwise(points):
        area += (point_a.imag + point_b.imag)*(point_a.real - point_b.real)
    return int(abs(area/2))

def part1(lines):
    steps = [(elem[0], int(elem[1])) for elem in STEP_REGEX.findall(lines)]
    return solve(steps)

def part2(lines):
    steps = [(elem[2][5], int(elem[2][:5], 16)) for elem in STEP_REGEX.findall(lines)]
    return solve(steps)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
