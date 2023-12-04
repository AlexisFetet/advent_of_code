"""
This file contains a code attempt for advent of code day 1
"""


import os


def parse(calories):
    """
    get input and computes total calories per elv
    """
    calories_elv = []
    sum_cal = 0
    for cal in calories:
        if cal:
            sum_cal += int(cal)
        else:
            calories_elv.append(sum_cal)
            sum_cal = 0
    calories_elv.append(sum_cal)
    return calories_elv


def sum_top3(calories):
    """
    compute sum of top3 carriers
    """
    cal_list = parse(calories)
    top1 = max(cal_list)
    cal_list.remove(top1)
    top2 = max(cal_list)
    cal_list.remove(top2)
    return top1 + top2 + max(cal_list)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {max(parse(my_tests))}")
    print(f"Answer test part2 : {sum_top3(my_tests)}")

    print(f"Answer part1 : {max(parse(my_input))}")
    print(f"Answer part2 : {sum_top3(my_input)}")
