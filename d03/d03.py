"""
This file contains a code attempt for advent of code day 3
"""

import re
import os

NUMBER_REGEX = re.compile(r"([0-9]+)")

characters = ['$', '&', '+', '-', '*', '/', '=', '@', '#', '%']


def part1(lines):
    sum_parts = 0
    matches = [NUMBER_REGEX.finditer(line) for line in lines]
    for line_nb, line_matches in enumerate(matches):
        for matched in line_matches:
            looking_for_symb = ''
            if line_nb != 0:
                looking_for_symb += lines[line_nb - 1][max(
                    0, matched.start() - 1):min(len(lines[0]), matched.end() + 1)]
            if matched.start() > 0:
                looking_for_symb += lines[line_nb][matched.start() - 1]
            if matched.end() < (len(lines[0]) - 1):
                looking_for_symb += lines[line_nb][matched.end()]
            if line_nb < (len(lines) - 1):
                looking_for_symb += lines[line_nb + 1][max(
                    0, matched.start() - 1):min(len(lines[0]), matched.end() + 1)]
            for symb in characters:
                if symb in looking_for_symb:
                    sum_parts += int(matched.group(0))
                    break
    return sum_parts


def part2(lines):
    matches = [re.finditer(r"\*", line) for line in lines]
    total = 0
    for line_nb, line_matches in enumerate(matches):
        for matched in line_matches:
            count = 0
            part_power = 1
            if line_nb > 0:
                found = NUMBER_REGEX.finditer(lines[line_nb - 1])
                for int_val in found:
                    if (int_val.start() - 1) <= matched.start() <= int_val.end():
                        part_power *= int(int_val.group(0))
                        count += 1
            if line_nb < (len(lines) - 1):
                found = NUMBER_REGEX.finditer(lines[line_nb + 1])
                for int_val in found:
                    if (int_val.start() - 1) <= matched.start() <= int_val.end():
                        part_power *= int(int_val.group(0))
                        count += 1
            found = NUMBER_REGEX.finditer(lines[line_nb][:matched.start()])
            for int_val in found:
                if int_val.end() == matched.start():
                    part_power *= int(int_val.group(0))
                    count += 1
                    break
            found = NUMBER_REGEX.finditer(lines[line_nb][matched.end():])
            for int_val in found:
                if int_val.start() == 0:
                    part_power *= int(int_val.group(0))
                    count += 1
                    break
            if count == 2:
                total += part_power
    return total


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
