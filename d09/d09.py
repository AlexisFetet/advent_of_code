"""
This file contains a code attempt for advent of code day 9
"""


import os


MOVES = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def too_far(head, tail):
    """
    return true if the tail is too far
    """
    delta_y = head[0]-tail[0]
    delta_x = head[1]-tail[1]
    valid = ((delta_y)**2 + (delta_x)**2) <= 2
    if not valid:
        correction = (max(min(1, delta_y), -1), max(min(1, delta_x), -1))
    else:
        correction = (0, 0)
    return valid, correction


def simulate_moves(moves, length):
    """
    simulate the moves and return the count of unique places visited
    """
    visited = set()
    rope = [[0, 0] for _ in range(length)]
    for move in moves:
        direction, repeat = move.split()
        repeat = int(repeat)
        for _ in range(repeat):
            vec = MOVES.get(direction)
            rope[0][0] += vec[0]
            rope[0][1] += vec[1]
            for indx in range(1, len(rope)):
                valid, correction = too_far(rope[indx - 1], rope[indx])
                if not valid:
                    rope[indx][0] += correction[0]
                    rope[indx][1] += correction[1]
            visited.add(tuple(rope[-1]))
    return len(visited)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {simulate_moves(my_tests, 2)}")
    print(f"Answer test part2 : {simulate_moves(my_tests, 10)}")

    print(f"Answer part1 : {simulate_moves(my_input, 2)}")
    print(f"Answer part2 : {simulate_moves(my_input, 10)}")
