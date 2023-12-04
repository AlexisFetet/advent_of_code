"""
This file contains a code attempt for advent of code day 1
"""


import os


def inc_nb(measures):
    """
    return number of increasing measures
    """
    inc = 0
    for k in range(1, len(measures)):
        inc += measures[k-1] < measures[k]
    return inc


def dec_nb(measures):
    """
    return number of decreasing measures
    """
    dec = 0
    for k in range(1, len(measures)):
        dec += measures[k-1] > measures[k]
    return dec


def equ_nb(measures):
    """
    return number of decreasing measures
    """
    equ = 0
    for k in range(1, len(measures)):
        equ += measures[k-1] == measures[k]
    return equ


def sliding_measure(measures):
    """
    return sliding measures from raw measures
    """
    sliding = []
    for k in range(len(measures)-2):
        sliding.append(measures[k]+measures[k+1]+measures[k+2])
    return sliding


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [int(value) for value in my_tests]
    my_input = [int(value) for value in my_input]

    print(f"Answer test part1 : {inc_nb(my_tests)}")
    print(f"Answer test part2 : {inc_nb(sliding_measure(my_tests))}")

    print(f"Answer part1 : {inc_nb(my_input)}")
    print(f"Answer part2 : {inc_nb(sliding_measure(my_input))}")
