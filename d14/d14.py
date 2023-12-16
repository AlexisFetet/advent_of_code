"""
This file contains a code attempt for advent of code day 14
"""

import numpy as np
import os


def tilt(board: np.ndarray):
    for x in range(np.shape(board)[0]):
        column = "".join(board[:, x])
        segments = []
        for support_seg in column.split("#"):
            rocks = support_seg.count('O')
            segments.append('O' * rocks + '.' * (len(support_seg) - rocks))
        board[:, x] = [char for char in "#".join(segments)]
    return board


def cycle(board):
    for _ in range(4):
        board = tilt(board)
        board = np.rot90(board, 1, (1,0))
    return board

def result(board):
    somme = 0
    for index, line in enumerate(board):
        unique, counts = np.unique(line, return_counts=True)
        somme += dict(zip(unique, counts)).get('O', 0) * \
            (np.shape(board)[0] - index)
    return somme


def part1(lines: list[str]):
    board = np.array([[char for char in line] for line in lines])
    board = tilt(board)
    return result(board)


def part2(lines: list[str], max_cycles=1000000):
    known_configs = {}
    board = np.array([[char for char in line] for line in lines])
    cycles = 0
    while cycles < max_cycles:
        board = cycle(board)
        cycles += 1
        known = known_configs.get(board.data.tobytes(), None)
        if known is None:
            print(f"added {cycles=}")
            known_configs[board.data.tobytes()] = cycles
        else:
            break
    period_start = known_configs[board.data.tobytes()]
    period_length = len(known_configs) - period_start + 1
    leftover = (max_cycles - period_start - 1) % period_length
    for _ in range(leftover - 1):
        board = cycle(board)
    return result(board)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
