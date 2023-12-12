"""
This file contains a code attempt for advent of code day 10
"""

from copy import deepcopy
import os

access = {
    'L': ((1, 0), (0, -1)),
    'J': ((1, 0), (0,  1)),
    'F': ((-1, 0), (0, -1)),
    '7': ((-1, 0), (0,  1)),
    '|': ((1, 0), (-1,  0)),
    '-': ((0, 1), (0, -1)),
    '.': ()
}


def direction(start, end):
    return (end[0] - start[0], end[1] - start[1])


def solve(lines: list[str], part=1):
    poi = []
    counter = 1
    start = (None, None)
    for (y, line) in enumerate(lines):
        if line.count('S') != 0:
            start = (y, lines[y].index('S'))
            break
    current = []
    previous_dir = []
    start_candidates = [(start[0] + y_offset, start[1] + x_offset)
                        for (y_offset, x_offset)
                        in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                        if (0 <= start[0] + y_offset < len(lines))
                        and (0 <= start[1] + x_offset < len(lines[0]))]
    for start_candidate in start_candidates:
        dir_ = direction(start, start_candidate)
        if dir_ in access[lines[start_candidate[0]][start_candidate[1]]]:
            current.append(start_candidate)
            previous_dir.append(dir_)
            poi.append(start_candidate)
    dir_ = direction(current[0], current[1])
    opp_dir = [(-previous_dir[0][0], -previous_dir[0][1]),
               (-previous_dir[1][0], -previous_dir[1][1])]
    for key_, value_ in access.items():
        if opp_dir[0] in value_ and opp_dir[1] in value_:
            lines[start[0]] = lines[start[0]][:start[1]] + \
                key_ + lines[start[0]][start[1] + 1:]
            break
    poi.append(start)
    while (current[0] != current[1]):
        counter += 1
        for index in [0, 1]:
            if access[lines[current[index][0]][current[index][1]]][0] == previous_dir[index]:
                new_dir = access[lines[current[index][0]]
                                 [current[index][1]]][1]
            else:
                new_dir = access[lines[current[index][0]]
                                 [current[index][1]]][0]
            new_point = (current[index][0] - new_dir[0],
                         current[index][1] - new_dir[1])
            previous_dir[index] = (- new_dir[0], - new_dir[1])
            current[index] = new_point
            poi.append(new_point)
    if part == 2:
        poi.sort()
        counter = 0
        for y in range(len(lines)):
            vertical = 0
            up_corner = False
            down_corner = False
            for x in range(len(lines[0])):
                current = lines[y][x]
                if(y, x) in poi:
                    if current == '|':
                        vertical += 1
                    elif current in ['F', '7']:
                        if down_corner:
                            down_corner = False
                        else:
                            if up_corner:
                                vertical += 1
                                up_corner = False
                            else:
                                down_corner = True
                    elif current in ['J', 'L']:
                        if up_corner:
                            up_corner = False
                        else:
                            if down_corner:
                                vertical += 1
                                down_corner = False
                            else:
                                up_corner = True
                else:
                    counter += int(vertical % 2)
    return counter


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {solve(deepcopy(my_input))}")
    print(f"Answer part2 : {solve(deepcopy(my_input), part=2)}")
