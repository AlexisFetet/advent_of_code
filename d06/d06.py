"""
This file contains a code attempt for advent of code day 6
"""


import os
from copy import deepcopy


def update(allfish):
    """
    update list of fish
    """
    newfish = allfish[0]
    allfish[7] += newfish
    for indx, fish in enumerate(allfish):
        if indx != 0:
            allfish[indx - 1] = fish
    allfish[8] = newfish
    return allfish


def simulate_(init, days):
    """
    simulate
    """
    for _ in range(days):
        init = update(init)
    return sum(init)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = list(map(int, my_tests[0].split(",")))
    my_input = list(map(int, my_input[0].split(",")))
    my_tests = [my_tests.count(k) for k in range(9)]
    my_input = [my_input.count(k) for k in range(9)]

    print(f"Answer test part1 : {simulate_(deepcopy(my_tests), 80)}")
    print(f"Answer test part2 : {simulate_(deepcopy(my_tests), 256)}")

    print(f"Answer part1 : {simulate_(deepcopy(my_input), 80)}")
    print(f"Answer part2 : {simulate_(deepcopy(my_input), 256)}")
