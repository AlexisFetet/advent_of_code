"""
This file contains a code attempt for advent of code day 3
"""


import os


def common_item(rucksack):
    """
    return the common element in both parts of the rucksack
    """
    pocket1 = set([char_ for char_ in rucksack[:len(rucksack)//2]])
    pocket2 = set([char_ for char_ in rucksack[len(rucksack)//2:]])
    return list(pocket1.intersection(pocket2))


def common_item_group(rucksacks):
    """
    return common element in all 3 bags
    """
    rucksack0 = set([char_ for char_ in rucksacks[0]])
    rucksack1 = set([char_ for char_ in rucksacks[1]])
    rucksack2 = set([char_ for char_ in rucksacks[2]])
    return list(rucksack0.intersection(rucksack1).intersection(rucksack2))


def item_priority(item):
    """
    compute item priority
    """
    value = (ord(item) - (64 - 26)) if (ord(item) < 95) else (ord(item) - 96)
    return value


def solve_part1(list_rucksack):
    """
    solve part1
    """
    common_items = [common_item(rucksack) for rucksack in list_rucksack]
    values = [sum([item_priority(item)
                  for item in rucksack])
              for rucksack in common_items]
    return sum(values)


def divide_work(list_rucksack):
    """
    devide list in groups of 3
    """
    return [list_rucksack[k*3:(k+1)*3] for k in range(len(list_rucksack)//3)]


def solve_part2(list_rucksacks):
    """
    solve part2
    """
    common_items = [common_item_group(group)
                    for group in divide_work(list_rucksacks)]
    values = [sum([item_priority(item)
                  for item in rucksack])
              for rucksack in common_items]
    return sum(values)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {solve_part1(my_tests)}")
    print(f"Answer test part2 : {solve_part2(my_tests)}")

    print(f"Answer part1 : {solve_part1(my_input)}")
    print(f"Answer part2 : {solve_part2(my_input)}")
