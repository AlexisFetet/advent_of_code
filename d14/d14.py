"""
This file contains a code attempt for advent of code day 14
"""


import os
import numpy as np
from more_itertools import pairwise


def build_grid(lists):
    """
    build the obstacle grid
    """
    max_x = max([max([coord[0] for coord in obstacle])
                for obstacle in lists])
    min_x = min([min([coord[0] for coord in obstacle])
                for obstacle in lists])
    max_y = max([max([coord[1] for coord in obstacle])
                for obstacle in lists])
    grid = np.zeros((max_y + 1, max_x - min_x + 1))
    for obstacle in lists:
        for start, end in pairwise(obstacle):
            [start, end] = sorted([start, end])
            for y in range(start[1], end[1] + 1):
                for x in range(start[0] - min_x, end[0] - min_x + 1):
                    grid[y, x] = 1
    grid = np.c_[np.zeros(max_y + 1), grid, np.zeros(max_y + 1)]
    offset = min_x - 1
    return grid, offset


def augment_grid(grid, offset):
    """
    augment the grid so that we can solve part2
    """
    grid = np.r_[grid, np.zeros((1, len(grid[0])))]
    expected_offset = 500 - len(grid)
    add_right = 2*len(grid) - len(grid[0]) - (offset - expected_offset) + 1
    for _ in range(offset - expected_offset):
        grid = np.c_[np.zeros(len(grid)), grid]
    for _ in range(add_right):
        grid = np.c_[grid, np.zeros(len(grid))]
    grid = np.r_[grid, np.array([[1 for _ in range(len(grid[0]))]])]
    return grid, expected_offset


def add_grain(grid, offset):
    """
    tries to add a grain to the grid, return true if grain
    was added successfully, false otherwise
    """
    placed = False
    current_y = -1
    current_x = 500 - offset
    while not placed:
        current_y += 1
        if current_y >= len(grid):
            break
        if grid[current_y, current_x] != 0:
            if grid[current_y, current_x - 1] != 0:
                if grid[current_y, current_x + 1] != 0:
                    if current_y - 1 == 0:
                        placed = 2
                        grid[current_y - 1, current_x] = 2
                        break
                    placed = True
                    grid[current_y - 1, current_x] = 2
                    break
                else:
                    current_x += 1
            else:
                current_x -= 1
    return placed, grid


def place_no_floor(obstacles):
    """
    return the max amount of sand grains that can fit in equilibrium
    """
    placed = 0
    grid, offset = build_grid(obstacles)
    equilibrium = True
    while equilibrium:
        equilibrium, grid = add_grain(grid, offset)
        placed += 1 if equilibrium else 0
    return placed


def place_floor(obstacles, file_name):
    """
    return the max amount of sand grains that can fit in equilibrium
    """
    placed = 0
    grid, offset = augment_grid(*build_grid(obstacles))
    equilibrium = True
    while equilibrium != 2 and equilibrium:
        equilibrium, grid = add_grain(grid, offset)
        placed += 1 if equilibrium else 0
    test = ""
    for line in grid:
        for char in line:
            if char == 0:
                test += "."
            if char == 1:
                test += "#"
            if char == 2:
                test += "o"
        test += "\n"
    with open(file_name, "w+", encoding="utf-8") as write_file:
        write_file.write(test)
    return placed


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [[[int(x) for x in coord.split(",")]
                for coord in line.split(" -> ")] for line in my_tests]
    my_input = [[[int(x) for x in coord.split(",")]
                for coord in line.split(" -> ")] for line in my_input]

    print(f"Answer test part1 : {place_no_floor(my_tests)}")
    print(f"Answer test part2 : {place_floor(my_tests, 'repr_test.txt')}")

    print(f"Answer part1 : {place_no_floor(my_input)}")
    print(f"Answer part2 : {place_floor(my_input, 'repr_input.txt')}")
