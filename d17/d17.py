"""
This file contains a code attempt for advent of code day 17
"""
from numpy import Infinity
from itertools import pairwise
import os


def heuristic(point, goal):
    return abs(goal.real - point.real) + abs(goal.imag - point.imag)


def dist_straight(points: list[complex]):
    if len(points) < 2:
        return 0
    dist = 1
    direction = (points[-1] - points[-2])
    remains = list(points[:-1])
    remains.reverse()
    pairs = pairwise(remains)
    for point_pair in pairs:
        if (point_pair[0] - point_pair[1]) == direction:
            dist += 1
        else:
            break
    return (dist, direction)


def generatrice_part1(current, width, height, gScore, weight):
    candidates = [current[-1] + delta for delta
                  in [1, 1j, -1, -1j]
                  if (0 <= (current[-1] + delta).real < width
                      and 0 <= (current[-1] + delta).imag < height
                      and dist_straight(current + (current[-1] + delta,))[0] < 4)]
    candidates = [(candidate,) for candidate
                  in candidates
                  if candidate not in current]
    candidates_score = [gScore[(current[-1], dist_straight(current))] + weight[int(candidate[-1].imag)][int(candidate[-1].real)]
                        for candidate in candidates]
    return zip(candidates, candidates_score)


def generatrice_part2(current, width, height, gScore, weight):
    if current == (0 + 0j,):
        new_directions = [1, 1j]
    else:
        current_direction = current[-2] - current[-1]
        if current_direction.real == 0:
            new_directions = [1 + 0j, -1 + 0j]
        else:
            new_directions = [1j, -1j]
    candidates = []
    for direction in new_directions:
        new_candidates = [tuple([current[-1] + direction*repeat for repeat in range(1,max_)]) for max_ in range(5,12)]
        for new_candidate in new_candidates:
            if 0 <= new_candidate[-1].real < width and 0 <= new_candidate[-1].imag < height:
                candidates.append(new_candidate)
    
    candidates = [candidate for candidate
                  in candidates
                  if candidate[-1] not in current]
    candidates_score = [gScore[(current[-1], dist_straight(current))] + sum([weight[int(point.imag)][int(point.real)] for point in candidate]) for candidate in candidates]
    return zip(candidates, candidates_score)

def A_Star(start: complex, goal: complex, height: int, width: int, weight: list[list[int]], generatrice=generatrice_part1, h=heuristic):
    openSet = set()
    openSet.add((start,))
    gScore = {(start, 0): 0}
    fScore = {(start): h(start, goal)}
    ite = 0

    while len(openSet) != 0:
        ite += 1
        if ite % 1000 == 0:
            print(len(openSet))

        current = min(openSet, key=lambda x: fScore[x[-1]])
        openSet.remove(current)
        if current[-1] == goal:
            continue

        candidates_generated = generatrice(
            current, width, height, gScore, weight)

        for candidate, score in candidates_generated:
            new_history = current + candidate
            if score < gScore.get((candidate[-1], dist_straight(new_history[-4:])), Infinity):
                gScore[(candidate[-1], dist_straight(new_history[-4:]))] = score
                if new_history[-4:] not in openSet:
                    openSet.add(new_history[-4:])
            if score + h(candidate[-1], goal) < fScore.get(candidate[-1], Infinity):
                fScore[candidate[-1]] = score + h(candidate[-1], goal)
    return int(fScore[goal])


def part1(lines):
    board = [[int(char) for char in line] for line in lines]
    start = 0 + 0j
    goal = (len(lines[0]) - 1) + (len(lines) - 1) * 1j
    return A_Star(start, goal, len(board), len(board[0]), board, generatrice_part1, heuristic)

def part2(lines):
    board = [[int(char) for char in line] for line in lines]
    start = 0 + 0j
    goal = (len(lines[0]) - 1) + (len(lines) - 1) * 1j
    return A_Star(start, goal, len(board), len(board[0]), board, generatrice_part2, heuristic)



if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_tests)}")
    print(f"Answer part2 : {part2(my_input)}")
