"""
This file contains a code attempt for advent of code day 1
"""

import os
import re

REGEX_COMMAND = re.compile(r"(?P<direction>[RL])(?P<amount>[0-9]+)")
START_VALUE = 50

def count_p2(current_value, old, computed_value, multiplier):
    return abs(divmod(computed_value, 100)[0]) - ((old == 0) and (multiplier == -1)) + (current_value == 0 and (multiplier == -1))

def solve_px(list_of_commands: list[str], counter):
    current_value = START_VALUE
    points = 0
    for command in list_of_commands:
        match_elem = REGEX_COMMAND.match(command)
        direction = match_elem["direction"]
        count = int(match_elem["amount"])
        multiplier = -1 if direction == 'L' else 1
        computed_value = current_value + multiplier * count
        old = current_value
        current_value = computed_value % 100
        points += counter(current_value, old, computed_value, multiplier)
    return points

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {solve_px(my_tests, lambda w, x, y, z: w == 0)}")

    print(f"Answer part1 : {solve_px(my_input, lambda w, x, y, z: w == 0)}")

    print(f"Answer exemple part2 : {solve_px(my_tests, count_p2)}")

    print(f"Answer part2 : {solve_px(my_input, count_p2)}")
