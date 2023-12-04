"""
This file contains a code attempt for advent of code day 8
"""


import os
from copy import deepcopy


def count_unique(sequence):
    """
    count the amount of digits using unique amount of segments
    """
    total = 0
    outputs = [line.split(" | ")[1].split() for line in sequence]
    for output in outputs:
        for value in output:
            if len(value) in (2, 3, 4, 7):
                total += 1
    return total


def construct_wiring(entry):
    """
    construct wiring
    """
    wiring = {}
    entry = ["".join(sorted([letter for letter in value])) for value in entry]
    length = [len(digit) for digit in entry]
    sets = [set([letter for letter in digit]) for digit in entry]

    digit_1 = (entry[length.index(2)], sets[length.index(2)])
    wiring.update({digit_1[0]: 1})
    digit_4 = (entry[length.index(4)], sets[length.index(4)])
    wiring.update({digit_4[0]: 4})
    digit_7 = (entry[length.index(3)], sets[length.index(3)])
    wiring.update({digit_7[0]: 7})
    digit_8 = (entry[length.index(7)], sets[length.index(7)])
    wiring.update({digit_8[0]: 8})

    # find top segment
    top = list(digit_7[1].difference(digit_1[1]))[0]

    # find 9
    augmented_4 = deepcopy(digit_4[1])
    augmented_4.add(top)
    digit_9 = [digit for digit in sets if
               (len(digit - augmented_4) == 1 and
                len(augmented_4 - digit) == 0)][0]
    digit_9 = (entry[sets.index(digit_9)], digit_9)
    wiring.update({digit_9[0]: 9})

    # find bottom segment
    bot = list(digit_9[1].difference(digit_4[1]).difference(digit_7[1]))[0]

    # find bottom left segment
    bot_left = list(digit_8[1].difference(digit_9[1]))[0]

    # find 3
    augmented_1 = deepcopy(digit_1[1])
    augmented_1.add(top)
    augmented_1.add(bot)
    digit_3 = [set_ for set_ in sets if
               (len(set_) == 5 and
                len(set_ - augmented_1) == 1)][0]
    digit_3 = (entry[sets.index(digit_3)], digit_3)
    wiring.update({digit_3[0]: 3})

    # find middle segment
    mid = list(digit_3[1].difference(augmented_1))[0]

    # find top left segment
    augmented_1.add(mid)
    top_left = list(digit_4[1].difference(augmented_1))[0]

    # find 6
    digit_6 = [digit for digit in sets if
               len(digit) == 6 and
               digit != digit_9[1] and
               len(digit.intersection(set([mid]))) == 1][0]
    digit_6 = (entry[sets.index(digit_6)], digit_6)
    wiring.update({digit_6[0]: 6})

    # find bottom right segment
    temp = set([top, bot, bot_left, top_left, mid])
    bot_right = list(digit_6[1].difference(temp))[0]

    # find top right segment
    top_right = list(digit_8[1].difference(digit_6[1]))[0]

    # build 0
    digit_0 = set([top, top_right, bot_right, bot, bot_left, top_left])
    digit_0 = (entry[sets.index(digit_0)], digit_0)
    wiring.update({digit_0[0]: 0})

    # build 2
    digit_2 = set([top, top_right, mid, bot_left, bot])
    digit_2 = (entry[sets.index(digit_2)], digit_2)
    wiring.update({digit_2[0]: 2})

    # build 5
    digit_5 = set([top, top_left, mid, bot_right, bot])
    digit_5 = (entry[sets.index(digit_5)], digit_5)
    wiring.update({digit_5[0]: 5})

    return wiring


def compute_value(sequence):
    """
    return sum of outputs
    """
    total = 0
    inputs = [line.split(" | ")[0].split() for line in sequence]
    outputs = [line.split(" | ")[1].split() for line in sequence]

    for input_, output in zip(inputs, outputs):
        output_value = 0
        wiring = construct_wiring(input_)
        for indx, value in enumerate(output):
            output_value += wiring.get(
                "".join(sorted(
                    [letter for letter in value]))) * 10 ** (3 - indx)
        total += output_value
    return total


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {count_unique(my_tests)}")
    print(f"Answer test part2 : {compute_value(my_tests)}")

    print(f"Answer part1 : {count_unique(my_input)}")
    print(f"Answer part2 : {compute_value(my_input)}")
