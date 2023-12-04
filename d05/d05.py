"""
This file contains a code attempt for advent of code day 5
"""


import os
import numpy as np


def evaluate_overlapping(lines, diag=False):
    """
    construct the grid
    """
    nb_line = max([max(x[0][0], x[1][0]) for x in lines]) + 1
    nb_col = max([max(x[0][1], x[1][1]) for x in lines]) + 1
    grid = np.zeros((nb_line, nb_col))
    for wind in lines:
        if wind[0][0] == wind[1][0]:
            for y in range(wind[0][1], wind[1][1] + 1):
                grid[y, wind[0][0]] += 1
        elif wind[0][1] == wind[1][1]:
            for x in range(wind[0][0], wind[1][0] + 1):
                grid[wind[0][1], x] += 1
        elif diag and wind[0][1] < wind[1][1]:
            coords = list(zip(range(wind[0][1], wind[1][1] + 1),
                              range(wind[0][0], wind[1][0] + 1)))
            for coord in coords:
                grid[coord[0], coord[1]] += 1
        elif diag:
            coords = list(zip(range(wind[0][1], wind[1][1] - 1, -1),
                              range(wind[0][0], wind[1][0] + 1)))
            for coord in coords:
                grid[coord[0], coord[1]] += 1
    return (grid > 1).sum()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [sorted([[int(x) for x in coords.split(",")]
                        for coords in wind.split(" -> ")])
                for wind in my_tests]

    my_input = [sorted([[int(x) for x in coords.split(",")]
                        for coords in wind.split(" -> ")])
                for wind in my_input]

    print(f"Answer test part1 : {evaluate_overlapping(my_tests)}")
    print(f"Answer test part2 : {evaluate_overlapping(my_tests, True)}")

    print(f"Answer part1 : {evaluate_overlapping(my_input)}")
    print(f"Answer part2 : {evaluate_overlapping(my_input, True)}")
