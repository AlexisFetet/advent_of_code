"""
This file contains a code attempt for advent of code day 8
"""

import itertools
import os

def squared_distance(item1, item2):
    return (item1[0] - item2[0]) ** 2 + (item1[1] - item2[1]) ** 2 + (item1[2] - item2[2]) ** 2

def find_entries_index(items, item1, item2):
    return [index for index, value in enumerate(items) if (item1[:-1] == value[:-1]) or (item2[:-1] == value[:-1])]

def change_group(items, new, old):
    for point in items:
        if point[3] == old:
            point[3] = new

def solve_p1(lines, max_= 1000):
    points = [list(map(int, line.split(','))) + [index] for index, line in enumerate(lines)]
    candidates = [(squared_distance(item1, item2), item1, item2) for item1, item2 in itertools.combinations(points, 2)]
    candidates.sort(key=lambda x: x[0])
    for pair in candidates[:max_]:
        item1_index, item2_index = find_entries_index(points, pair[1], pair[2])
        item1, item2 = points[item1_index], points[item2_index]
        group = [item1[3], item2[3]]
        group.sort()
        change_group(points, *group)
    groups = [item[3] for item in points]
    ranking = [(item, groups.count(item)) for item in set(groups)]
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[0][1] * ranking[1][1] * ranking[2][1]

def solve_p2(lines):
    points = [list(map(int, line.split(','))) + [index] for index, line in enumerate(lines)]
    candidates = [(squared_distance(item1, item2), item1, item2) for item1, item2 in itertools.combinations(points, 2)]
    candidates.sort(key=lambda x: x[0])
    for pair in candidates:
        item1_index, item2_index = find_entries_index(points, pair[1], pair[2])
        item1, item2 = points[item1_index], points[item2_index]
        group = [item1[3], item2[3]]
        group.sort()
        change_group(points, *group)
        groups = [item[3] for item in points]
        if len(set(groups)) == 1:
            return item1[0] * item2[0]

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {solve_p1(my_tests, 10)}")
    print(f"Answer part1 : {solve_p1(my_input)}")
    print(f"Answer exemple part2 : {solve_p2(my_tests)}")
    print(f"Answer part2 : {solve_p2(my_input)}")
