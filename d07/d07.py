"""
This file contains a code attempt for advent of code day 7
"""


import os
import scipy


def lowest_cost1(positions):
    """
    answer to question1
    """

    def cost1(x):
        return sum([abs(pos - x) for pos in positions])

    ans1 = scipy.optimize.minimize(cost1, x0=int(len(positions)/2))
    return round(cost1(round(ans1.x[0])))


def lowest_cost2(positions):
    """
    answer to question2
    """

    def cost2(x):
        return sum([abs(pos - x)*(abs(pos - x)+1)/2 for pos in positions])

    ans2 = scipy.optimize.minimize(cost2, x0=int(len(positions)/2))
    return round(cost2(round(ans2.x[0])))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [int(x) for x in my_tests[0].split(",")]
    my_input = [int(x) for x in my_input[0].split(",")]

    print(f"Answer part1 : {lowest_cost1(my_tests)}")
    print(f"Answer part2 : {lowest_cost2(my_tests)}")

    print(f"Answer part1 : {lowest_cost1(my_input)}")
    print(f"Answer part2 : {lowest_cost2(my_input)}")
