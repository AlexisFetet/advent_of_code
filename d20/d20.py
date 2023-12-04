"""
This file contains a code attempt for advent of code day 20
"""


import os
from copy import deepcopy


DECRIPTION_KEY = 811589153


def mix(my_list: list[int]):
    """
    mix the list
    """
    answer = deepcopy(my_list)
    answer = [(element, i) for i, element in enumerate(answer)]
    temp = deepcopy(answer)
    for element in temp:
        init_indx = answer.index(element)
        final_indx = (init_indx + element[0]) % (len(my_list) - 1)
        answer.remove(element)
        answer = answer[:final_indx] + [element[0]] + answer[final_indx:]
    return answer


def grove(my_list):
    """
    return the grove value
    """
    offset = my_list.index(0)
    return (my_list[(offset + 1000) % len(my_list)] +
            my_list[(offset + 2000) % len(my_list)] +
            my_list[(offset + 3000) % len(my_list)])


def decript(my_list):
    """
    solve part2
    """
    answer = deepcopy(my_list)
    answer = list(map(lambda x: x * DECRIPTION_KEY, answer))
    answer = [(element, i) for i, element in enumerate(answer)]
    temp = deepcopy(answer)
    for _ in range(10):
        for element in temp:
            init_indx = answer.index(element)
            final_indx = (init_indx + element[0]) % (len(my_list) - 1)
            answer.remove(element)
            answer = answer[:final_indx] + [element] + answer[final_indx:]
    return grove([element[0] for element in answer])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = list(map(int, file.read().splitlines()))

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = list(map(int, file.read().splitlines()))

    print(f"Answer test part1 : {grove(mix(my_tests))}")
    print(f"Answer test part2 : {decript(my_tests)}")

    print(f"Answer part1 : {grove(mix(my_input))}")
    print(f"Answer part2 : {decript(my_input)}")
