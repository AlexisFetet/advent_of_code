"""
This file contains a code attempt for advent of code day 5
"""


import os
import re
import queue

MOVES = re.compile(r"move ([0-9]+) from ([0-9]+) to ([0-9]+)")
PILES = re.compile(r"(\s{4}|[A-Z])")


def parse_input(input_: list[str]):
    """
    parse the problem
    """
    raw = "".join(input_)
    end_of_piles = input_.index("")
    move_instructions = [[int(instr[0]), int(instr[1])-1, int(instr[2])-1]
                         for instr in MOVES.findall(raw)]
    instruction_piles = [PILES.findall(input_[k])
                         for k in range(end_of_piles-1)]
    instruction_piles.reverse()
    piles = [queue.LifoQueue() for _ in range(len(instruction_piles[0]))]
    for instruction in instruction_piles:
        for indx, elem in enumerate(instruction):
            if elem != '    ':
                piles[indx].put(elem)
    return (piles, move_instructions)


def exec_instr(piles: list[queue.LifoQueue], instr_list):
    """
    applies all instructions
    """
    for instr in instr_list:
        for _ in range(instr[0]):
            elem = piles[instr[1]].get()
            piles[instr[2]].put(elem)
    return piles


def exec_instr_cratemover(piles: list[queue.LifoQueue], instr_list):
    """
    applies all instructions
    """
    for instr in instr_list:
        to_move = []
        for _ in range(instr[0]):
            to_move.append(piles[instr[1]].get())
        to_move.reverse()
        for elem in to_move:
            piles[instr[2]].put(elem)
    return piles


def get_message(piles):
    """
    get message
    """
    return "".join([pile.get() for pile in piles])


def solve_part1(input_):
    """
    solve part 1
    """
    return get_message(exec_instr(*parse_input(input_)))


def solve_part2(input_):
    """
    solve part 2
    """
    return get_message(exec_instr_cratemover(*parse_input(input_)))


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
    print(f"Answer test part2 : {solve_part2(my_input)}")
