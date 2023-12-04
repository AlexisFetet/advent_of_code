"""
This file contains a code attempt for advent of code day 12
"""


import math
import os

import numpy as np

DIRECTIONS = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
]


def indx2coords(indx, height):
    """
    return coords from index
    """
    return (indx % height, indx // height)


def coords2indx(coord_x, coord_y, height):
    """
    return index from coords
    """
    return (coord_y * height + coord_x)


def cost1(indx1, indx2, grid):
    """
    return cost between indx1 et indx2
    """
    coords1 = indx2coords(indx1, len(grid))
    coords2 = indx2coords(indx2, len(grid))
    if (ord(grid[coords2[0], coords2[1]]) -
       ord(grid[coords1[0], coords1[1]])) <= 1:
        return 1
    return math.inf


def cost2(indx1, indx2, grid):
    """
    return cost between indx1 et indx2
    """
    coords1 = indx2coords(indx1, len(grid))
    coords2 = indx2coords(indx2, len(grid))
    if (ord(grid[coords2[0], coords2[1]]) -
       ord(grid[coords1[0], coords1[1]])) >= -1:
        return 1
    return math.inf


def shortest_path(array, part):
    """
    return the length of the shortest path
    """
    grid = np.array(array)
    shape = np.shape(grid)

    cost = cost1 if part == 1 else cost2

    table = [math.inf for _ in range(shape[0]*shape[1])]
    not_visited = list(range(shape[0]*shape[1]))

    coords_start = list(zip(*np.where(grid == "S")))[0]
    coords_end = list(zip(*np.where(grid == "E")))[0]
    grid[coords_start[0], coords_start[1]] = "a"
    grid[coords_end[0], coords_end[1]] = "z"

    if part == 1:
        indx_end = [coords2indx(*coords_end, shape[0])]
        table[coords2indx(*coords_start, shape[0])] = 0
    else:
        indx_end = [coords2indx(*x, shape[0]) for x
                    in list(zip(*np.where(grid == "a")))]
        table[coords2indx(*coords_end, shape[0])] = 0

    while len(not_visited) > 0:
        best_cost = min(table)
        best_idnx = table.index(best_cost)
        if best_idnx in indx_end:
            break
        else:
            not_visited.remove(best_idnx)
            table[best_idnx] = math.inf
        for vect in DIRECTIONS:
            test = list(indx2coords(best_idnx, shape[0]))
            test[0] += vect[0]
            test[1] += vect[1]
            if not 0 <= test[0] < shape[0] or not 0 <= test[1] < shape[1]:
                continue
            indx = coords2indx(test[0], test[1], shape[0])
            if indx in not_visited:
                add_cost = best_cost + cost(best_idnx, indx, grid)
                if add_cost < table[indx]:
                    table[indx] = add_cost
    return min(table[indx] for indx in indx_end)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [[char for char in line] for line in my_tests]
    my_input = [[char for char in line] for line in my_input]

    print(f"Answer part1 : {shortest_path(my_tests, 1)}")
    print(f"Answer part2 : {shortest_path(my_tests, 2)}")

    print(f"Answer part1 : {shortest_path(my_input, 1)}")
    print(f"Answer part2 : {shortest_path(my_input, 2)}")
