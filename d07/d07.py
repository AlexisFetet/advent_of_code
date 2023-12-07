"""
This file contains a code attempt for advent of code day 7
"""


import os


def combination_value(string):
    return sum(map(lambda x: pow(x, 2), [string.count(elem) for elem in set(string)]))


def combination_value2(string):
    J_count = string.count('1')
    string = string.replace('1', '')
    to_process = []
    if 5 == J_count:
        to_process = [5]
    else:
        to_process = sorted([string.count(elem) for elem in set(string)])
        to_process[-1] += J_count
    return sum(map(lambda x: pow(x, 2), to_process))


def key_func(x):
    return (combination_value(x[0]), x[0])


def key_func2(x):
    return (combination_value2(x[0]), x[0])


def part1(lines: list[str]):
    game = [(elem[0].replace('A', 'E').replace('K', 'D').replace('Q', 'C').replace('J', 'B').replace('T', 'A'), int(elem[1]))
            for elem in [line.split() for line in lines]]
    game = sorted(game, key=key_func)
    return sum([(indx + 1) * value[1] for (indx, value) in enumerate(game)])


def part2(lines: list[str]):
    game = [(elem[0].replace('A', 'E').replace('K', 'D').replace('Q', 'C').replace('J', '1').replace('T', 'A'), int(elem[1]))
            for elem in [line.split() for line in lines]]
    game = sorted(game, key=key_func2)
    return sum([(indx + 1) * value[1] for (indx, value) in enumerate(game)])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
