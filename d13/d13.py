"""
This file contains a code attempt for advent of code day 13
"""


import os
from copy import deepcopy


def compare(list1, list2):
    """
    return true if list1 <= list2
    """
    temp1 = deepcopy(list1)
    temp2 = deepcopy(list2)
    for a, b in zip(list1, list2):
        temp1.remove(a)
        temp2.remove(b)
        if isinstance(a, int) and isinstance(b, int):
            if a > b:
                return 0
            if a < b:
                return 1
        elif isinstance(a, list) and isinstance(b, list):
            temp = compare(a, b)
            if temp != 2:
                return temp
        elif isinstance(a, int):
            temp = compare([a], b)
            if temp != 2:
                return temp
        else:
            temp = compare(a, [b])
            if temp != 2:
                return temp
    if len(temp1) == 0 and len(temp2) != 0:
        return 1
    if len(temp2) == 0 and len(temp1) != 0:
        return 0
    return 2


def sort(packets):
    """
    sort the packets using insertion sort
    """
    sorted_packets = [packets[0]]
    for k in range(1, len(packets)):
        current = packets[k]
        placed = False
        for indx, packet in enumerate(sorted_packets):
            if not compare(packet, current):
                placed = True
                sorted_packets = (sorted_packets[:indx] +
                                  [current] + sorted_packets[indx:])
                break
        if placed:
            continue
        else:
            sorted_packets.append(current)
    return sorted_packets


def decoder_key(packet_pairs):
    """
    return the decoder key
    """
    to_sort = []
    for pair in packet_pairs:
        to_sort.append(pair[0])
        to_sort.append(pair[1])
    to_sort.append([[2]])
    to_sort.append([[6]])
    sorted_packets = sort(to_sort)
    return ((1 + sorted_packets.index([[2]])) *
            (1 + sorted_packets.index([[6]])))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().split("\n\n")

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().split("\n\n")

    my_tests = [[eval(line) for line in pair.split()] for pair in my_tests]
    my_input = [[eval(line) for line in pair.split()] for pair in my_input]

    test_temp = sum([(indx+1) * compare(*lists)
                    for indx, lists in enumerate(my_tests)])
    print(f"Answer test part1 : {test_temp}")
    print(f"Answer test part2 : {decoder_key(my_tests)}")

    input_temp = sum([(indx+1) * compare(*lists)
                     for indx, lists in enumerate(my_input)])
    print(f"Answer test part1 : {input_temp}")
    print(f"Answer test part2 : {decoder_key(my_input)}")
