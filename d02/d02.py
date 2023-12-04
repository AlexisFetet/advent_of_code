"""
This file contains a code attempt for advent of code day 2
"""


import os

SCORE = {
    "X": 1,  # rock
    "Y": 2,  # paper
    "Z": 3,  # scissors
}

BEATS = {
    "A": "Z",  # rock beats scissors
    "B": "X",  # paper beats rock
    "C": "Y",  # scissors beat paper
}

BEATEN_BY = {
    "A": "Y",  # rock beaten by paper
    "B": "Z",  # paper beaten by scissors
    "C": "X",  # scissors beaten by rock<
}

SAME_PLAY = {
    "A": "X",  # rock
    "B": "Y",  # paper
    "C": "Z",  # scissors
}


def compute_score(game):
    """
    computes the score of the player playing with XYZ
    """
    score = 0
    for _round in game:

        score += SCORE.get(_round[1])

        if SAME_PLAY.get(_round[0]) == _round[1]:
            score += 3
            continue
        if BEATEN_BY.get(_round[0]) == _round[1]:
            score += 6
            continue
    return score


def redefine_game(game):
    """
    recreates game according to part 2
    """
    for _round in game:
        if _round[1] == "X":
            _round[1] = BEATS.get(_round[0])
            continue
        elif _round[1] == "Y":
            _round[1] = SAME_PLAY.get(_round[0])
            continue
        else:
            _round[1] = BEATEN_BY.get(_round[0])
    return game


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [_round.split() for _round in my_tests]
    my_input = [_round.split() for _round in my_input]

    print(f"Answer test part1 : {compute_score(my_tests)}")
    print(f"Answer test part2 : {compute_score(redefine_game(my_tests))}")

    print(f"Answer part1 : {compute_score(my_input)}")
    print(f"Answer part2 : {compute_score(redefine_game(my_input))}")
