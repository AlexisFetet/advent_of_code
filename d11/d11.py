"""
This file contains a code attempt for advent of code day 11
"""

from itertools import combinations
import os


def find(lines):
    const = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                const.append((y, x))
    return const


def solve(lines, factor):
    points = find(lines)
    ys = [point[0] for point in points]
    xs = [point[1] for point in points]
    ys_offset = [0 for _ in points]
    xs_offset = [0 for _ in points]
    for y in range(len(lines)):
        if y not in ys:
            for index, og_y in enumerate(ys):
                if og_y > y:
                    ys_offset[index] += factor
    for x in range(len(lines[0])):
        if x not in xs:
            for index, og_x in enumerate(xs):
                if og_x > x:
                    xs_offset[index] += factor
    new_points = []
    for (offset_y, offset_x, point) in zip(ys_offset, xs_offset, points):
        new_points.append((point[0] + offset_y, point[1] + offset_x))
    pairs = combinations(new_points, 2)
    accu = 0
    for pair in pairs:
        pair = sorted(pair)
        accu += abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
    return accu


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {solve(my_input, 1)}")
    print(f"Answer part2 : {solve(my_input, 999999)}")
