"""
This file contains a code attempt for advent of code day 15
"""


import os


def hash_(string: str):
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current = current % 256
    return current


def part1(lines):
    return sum(map(hash_, lines[0].split(',')))


def part2(lines):
    boxes = {}
    last_values = {}
    for op in lines[0].split(','):
        if '=' in op:
            op_split = op.split('=')
            lens_label = op_split[0]
            lens_foc_len = int(op_split[1])
            hashed_label = hash_(lens_label)
            if hashed_label not in boxes.keys():
                boxes[hashed_label] = [lens_label]
            elif lens_label not in boxes[hashed_label]:
                boxes[hashed_label].append(lens_label)
            last_values[lens_label] = lens_foc_len
        elif '-' in op:
            op_split = op.split('-')
            lens_label = op_split[0]
            hashed_label = hash_(lens_label)
            if hashed_label in boxes.keys():
                if lens_label in boxes[hashed_label]:
                    boxes[hashed_label].remove(lens_label)
    somme = 0
    for hashed_value, box in boxes.items():
        for index, lens in enumerate(box):
            somme += (hashed_value + 1) * (index + 1) * last_values[lens]
    return somme


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
