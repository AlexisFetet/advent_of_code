"""
This file contains a code attempt for advent of code day 2
"""

import re
import os
from functools import reduce

PLAYED_REGEX = re.compile(r"([0-9]+) (blue|red|green)+")
GAME_NUMBER_REGEX = re.compile(r"Game ([0-9]+)")


def value_game(game, func=max):
    played = PLAYED_REGEX.findall(game)
    sets = {
        "green": [],
        "red": [],
        "blue": []
    }
    for shown in played:
        sets[shown[1]].append(int(shown[0]))
    return {key: func(value) for key, value in sets.items()}


def valid_game(game, tot_green, tot_red, tot_blue):
    max_played = value_game(game, max)
    return ((max_played["green"] <= tot_green) and (max_played["red"] <= tot_red) and (max_played["blue"] <= tot_blue))


def part1(games, tot_green=13, tot_red=12, tot_blue=14):
    return sum([int(GAME_NUMBER_REGEX.findall(game)[0]) if valid_game(game, tot_green, tot_red, tot_blue) else 0 for game in games])


def part2(games):
    min_played = [value_game(game, max) for game in games]
    optimal_count = [list(min_set.values()) for min_set in min_played]
    set_power = [reduce(lambda x, y: x*y, game) for game in optimal_count]
    return sum(set_power)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
