"""
This file contains a code attempt for advent of code day 8
"""


import os
import numpy as np
from copy import deepcopy


def evaluate_visibility(row_slice: list):
    """
    evaluate visibility of last tree
    """
    sample = deepcopy(row_slice)
    sample.reverse()
    sample[0] -= 1
    max_high = max(sample)
    visible = max_high == sample[0]
    higher_trees = [k for k in sample if k > sample[0]]

    return (visible,
            sample.index(higher_trees[0]) if not visible else len(sample) - 1)


def evaluate_forest(forest):
    """
    solve part1
    """
    forest_arr = np.array(forest)
    forest_size = np.shape(forest_arr)
    tot_visible = 0
    max_view = 0
    for coord_y in range(forest_size[0]):
        for coord_x in range(forest_size[1]):
            if (coord_x == 0 or coord_x == forest_size[1] - 1
               or coord_y == 0 or coord_y == forest_size[0] - 1):
                tot_visible += 1
                continue

            visible = False
            current_view = 1

            current = list(forest_arr[coord_y, coord_x:])
            current.reverse()
            vis_test = evaluate_visibility(current)
            current_view *= vis_test[1]
            if vis_test[0]:
                visible = True

            vis_test = evaluate_visibility(list(forest_arr[coord_y,
                                                           :coord_x + 1]))
            current_view *= vis_test[1]
            if vis_test[0]:
                visible = True

            current = list(forest_arr[coord_y:, coord_x])
            current.reverse()
            vis_test = evaluate_visibility(current)
            current_view *= vis_test[1]
            if vis_test[0]:
                visible = True

            vis_test = evaluate_visibility(list(forest_arr[:coord_y + 1,
                                                           coord_x]))
            current_view *= vis_test[1]
            if vis_test[0]:
                visible = True

            if visible:
                tot_visible += 1

            if current_view > max_view:
                max_view = current_view

    return tot_visible, max_view


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [[int(digit) for digit in row] for row in my_tests]
    my_input = [[int(digit) for digit in row] for row in my_input]

    test_result = evaluate_forest(my_tests)
    print(f"Answer test part1 : {test_result[0]}")
    print(f"Answer test part2 : {test_result[1]}")

    input_result = evaluate_forest(my_input)
    print(f"Answer part1 : {input_result[0]}")
    print(f"Answer part2 : {input_result[1]}")
