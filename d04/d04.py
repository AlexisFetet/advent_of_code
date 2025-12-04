"""
This file contains a code attempt for advent of code day 4
"""


import os

def solve_p1(lines):
    width = len(lines[0])
    height = len(lines)
    valids = set()
    for x in range(width):
        for y in range(height):
            if lines[y][x] != '@':
                continue
            local_counter = 0
            for x_inc in range(-1, 2):
                for y_inc in range(-1, 2):
                    if x_inc == y_inc == 0:
                        continue
                    if (0 <= x_inc + x < width) and (0 <= y_inc + y < height):
                        local_counter += (lines[y_inc + y][x_inc + x] == '@')
            if local_counter < 4:
                valids.add((y, x))
    return valids

def solve_p2(lines):
    counter = 0
    valids = solve_p1(lines)
    while valids:
        counter += len(valids)
        for (y, x) in valids:
            lines[y] = lines[y][:x] + '.' + lines[y][x + 1:]
        valids = solve_p1(lines)
    return counter

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {len(solve_p1(my_tests))}")
    print(f"Answer part1 : {len(solve_p1(my_input))}")
    print(f"Answer exemple part2 : {solve_p2(my_tests)}")
    print(f"Answer part2 : {solve_p2(my_input)}")
