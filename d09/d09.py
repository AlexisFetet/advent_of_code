"""
This file contains a code attempt for advent of code day 9
"""

import functools
import itertools
import os

def area(point1, point2):
    return (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)

def solve_p1(lines):
    return max(map(lambda pair: area(*pair), itertools.combinations([tuple(map(int, line.split(','))) for line in lines], 2)))

def is_in_rectangle(corner1, corner2, point):
    return (point[0] > min(corner1[0], corner2[0])) \
       and (point[1] > min(corner1[1], corner2[1])) \
       and (point[0] < max(corner1[0], corner2[0])) \
       and (point[1] < max(corner1[1], corner2[1]))

def is_any_in_rectangle(corner1, corner2, points):
    return functools.reduce(lambda x,y: x or y, map(lambda point: is_in_rectangle(corner1, corner2, point), points))

def best_other(corner1, points):
    return max([area(corner1, point) for point in points if not is_any_in_rectangle(corner1, point, points)])

def solve_p2(lines):
    points = [tuple(map(int, line.split(','))) for line in lines]
    return max(best_other(points[248], points[:248]), best_other(points[249], points[250:]))

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {solve_p1(my_tests)}")
    print(f"Answer part1 : {solve_p1(my_input)}")
    print(f"Answer part2 : {solve_p2(my_input)}")
