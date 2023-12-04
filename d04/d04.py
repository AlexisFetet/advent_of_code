"""
This file contains a code attempt for advent of code day 4
"""

import re
import os

GAME_REGEX = re.compile(
    r"Card(?:\s)*([0-9]+): ((?:(?:\s)*(?:[0-9]+))+) \| ((?:(?:\s)*(?:[0-9]+))+)")
NUMBER_REGEX = re.compile(r"([0-9]+)")


def process(cards):
    return [len(set([int(x) for x in NUMBER_REGEX.findall(card[1])])
                .intersection(set([int(x) for x in NUMBER_REGEX.findall(card[2])])))
            for card in GAME_REGEX.findall("".join(cards))
            ]


def part1(cards):
    temp = process(cards)
    return sum([int(pow(2, (elem - 1))) for elem in temp])


def part2(cards):
    temp = [[1, elem] for elem in process(cards)]
    for index, elem in enumerate(temp):
        for offset in range(elem[1]):
            if index + offset + 1 < len(temp):
                temp[index + offset + 1][0] += temp[index][0]
    return sum([elem[0] for elem in temp])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
