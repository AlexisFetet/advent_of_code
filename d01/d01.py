"""
This file contains a code attempt for advent of code day 1
"""

import re
import os

DIGIT_DICT = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9
}

DIGIT_SPELT_DICT = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def first_value(line: str, revert: bool = False, keymap: dict[str: int] = DIGIT_DICT):

    if (revert):
        working_keymap = {key[::-1]: value for (key, value) in keymap.items()}
        working_line = line[::-1]
    else:
        working_keymap = keymap
        working_line = line

    matches = [re.search(f"({word})", working_line)
               for word in working_keymap.keys()]
    first = min(matches, key=lambda x: x.start()
                if x is not None else len(line))

    return working_keymap[first.string[first.span()[0]:first.span()[1]]]


def line_value(line, part):
    if 1 == part:
        return first_value(line) * 10 + first_value(line, revert=True)
    else:
        return first_value(line, keymap=DIGIT_SPELT_DICT | DIGIT_DICT) * 10 + first_value(line, revert=True, keymap=DIGIT_SPELT_DICT | DIGIT_DICT)


def total_value(lines, part):
    return sum([line_value(line, part) for line in lines])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {total_value(my_input, 1)}")
    print(f"Answer part2 : {total_value(my_input, 2)}")
