# pylint: disable=E1123

"""
This file contains a code attempt for advent of code day 4
"""


import os

import numpy as np


class Grid():
    """
    this class represents a grid
    """

    def __init__(self, array) -> None:
        self.array = array

    def is_winning(self, coords):
        """
        checks if board won
        """
        return (sum(self.array[coords[0], :]) == -5 or
                sum(self.array[:, coords[1]]) == -5)

    def play(self, val):
        """
        play a value on the grid
        """
        result = np.where(self.array == val)
        coords = list(zip(result[0], result[1]))
        win = False
        if coords:
            self.array[coords[0][0], coords[0][1]] = -1
            win = self.is_winning(coords[0])
        return win


def solve_part1(grid_list, draw):
    """
    find out the score of the winning board
    """
    grids = [Grid(np.array(grid)) for grid in grid_list]
    last_value = None
    winning_grid = None
    won = False
    for value in draw:
        if not won:
            for grid in grids:
                if grid.play(value):
                    winning_grid = grid
                    last_value = value
                    won = True
                    break
    result = np.sum(winning_grid.array,
                    where=(winning_grid.array != -1)) * last_value
    return result


def solve_part2(grid_list, draw):
    """
    find out the score of the last winning board
    """
    grids = [Grid(np.array(grid)) for grid in grid_list]
    last_value = None
    last_winning_grid = None
    for value in draw:
        to_remove = []
        for grid in grids:
            if grid.play(value):
                last_value = value
                last_winning_grid = grid
                to_remove.append(grid)
        for grid in to_remove:
            grids.remove(grid)
        if len(grids) == 0:
            break
    result = np.sum(last_winning_grid.array,
                    where=(last_winning_grid.array != -1)) * last_value
    return result


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_test_draw = [int(val) for val in my_tests[0].split(",")]
    my_test_grids = []
    for k in range(len(my_tests)//6):
        my_test_grids.append([[int(char) for char in line.split()]
                             for line in my_tests[2+k*6:1+(k+1)*6]])

    my_draw = [int(val) for val in my_input[0].split(",")]
    my_grids = []
    for k in range(len(my_input)//6):
        my_grids.append([[int(char) for char in line.split()]
                        for line in my_input[2+k*6:1+(k+1)*6]])

    print(f"Answer test part1 : {solve_part1(my_test_grids, my_test_draw)}")
    print(f"Answer test part2 : {solve_part2(my_test_grids, my_test_draw)}")

    print(f"Answer part1 : {solve_part1(my_grids, my_draw)}")
    print(f"Answer part2 : {solve_part2(my_grids, my_draw)}")
