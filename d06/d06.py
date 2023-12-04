"""
This file contains a code attempt for advent of code day 6
"""


import os


def start_of_packet(packet, nb_):
    """
    return index of start of communication + 1
    """
    for indx in range(4, len(packet)):
        if len(set(packet[indx-nb_: indx])) == nb_:
            return indx


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    for test in my_tests:
        print(f"packet : {test}")
        print(f"Answer test part1 : {start_of_packet(test, 4)}")
        print(f"Answer test part2 : {start_of_packet(test, 14)}")

    print("my key :")
    print(f"Answer part1 : {start_of_packet(my_input[0], 4)}")
    print(f"Answer part2 : {start_of_packet(my_input[0], 14)}")
