"""
This file contains a code attempt for advent of code day 3
"""


import os
import numpy as np


def most_common(bit_list):
    """
    return the value of the most present bit
    """
    c_1 = sum(bit_list)
    return 1 if c_1 >= len(bit_list)/2 else 0


def least_common(bit_list):
    """
    return the value of the least present bit
    """
    c_1 = sum(bit_list)
    return 0 if c_1 >= len(bit_list)/2 else 1


def compute_gamma(diagnostic):
    """
    compute the binary representation of gamma rate value of a diagnostic
    """
    result = "0b"
    for k in range(len(diagnostic[0])):
        result += str(most_common(diagnostic[:, k]))
    return result


def compute_epsilon(gamma):
    """
    compute the binary representation of epsilon rate value of a diagnostic
    """
    result = "0b"
    for bit in gamma[2:]:
        result += "1" if bit == "0" else "0"
    return result


def compute_power(diagnostic):
    """
    compute the power consumption
    """
    gamma = compute_gamma(diagnostic)
    epsilon = compute_epsilon(gamma)
    return int(gamma, 2)*int(epsilon, 2)


def sort(diagnostic, ref_bit, ref_position):
    """
    remove all words with bit different than ref_bit in position ref_position
    """
    return np.array([word for word in diagnostic
                    if word[ref_position] == ref_bit])


def compute_oxygen(diagnostic):
    """
    compute the oxygen generator rating
    """
    ref_pos = 0
    while len(diagnostic) != 1:
        diagnostic = sort(diagnostic,
                          most_common(diagnostic[:, ref_pos]),
                          ref_pos)
        ref_pos += 1
    return "0b" + "".join([str(char) for char in diagnostic[0]])


def compute_co2(diagnostic):
    """
    compute the c02 scubber rating
    """
    ref_pos = 0
    while len(diagnostic) != 1:
        diagnostic = sort(diagnostic,
                          least_common(diagnostic[:, ref_pos]),
                          ref_pos)
        ref_pos += 1
    return "0b" + "".join([str(char) for char in diagnostic[0]])


def compute_support(diagnostic):
    """
    compute the life support rating
    """
    oxygen = compute_oxygen(diagnostic)
    co2 = compute_co2(diagnostic)
    return int(oxygen, 2)*int(co2, 2)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = np.array([[int(char) for char in word] for word in my_tests])
    my_input = np.array([[int(char) for char in word] for word in my_input])

    print(f"Answer test part1 : {compute_power(my_tests)}")
    print(f"Answer test part2 : {compute_support(my_tests)}")

    print(f"Answer part1 : {compute_power(my_input)}")
    print(f"Answer part2 : {compute_support(my_input)}")
