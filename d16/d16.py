"""
This file contains a code attempt for advent of code day 16
"""


import os
import re
from copy import deepcopy
from math import inf

import numpy as np

VALVE = re.compile(r"([A-Z]{2})+")
FLOW = re.compile(r"[0-9]+")


def parse_input(lists):
    """
    parse an input and produces a dict of valves
    """
    valves = {}
    for valve in lists:
        current_valve = VALVE.findall(valve)
        current_flow = int(FLOW.findall(valve)[0])
        valves.update({current_valve[0]: [current_flow, current_valve[1:]]})
    return valves


def dijkstra(valves: dict[str:list[int, list[str]]], start: str):
    """
    find shortest distance from start to all points
    """
    all_keys = list(valves.keys())
    not_visited = list(valves.keys())
    cost = [inf] * len(not_visited)
    cost[not_visited.index(start)] = 0
    all_cost = [deepcopy(cost)]

    while len(not_visited) != 0:
        best_cost = min(cost)
        best_indx = cost.index(best_cost)
        best_valve = all_keys[best_indx]
        not_visited.remove(best_valve)
        cost[best_indx] = inf
        for near_valve in valves[best_valve][1]:
            if near_valve in not_visited:
                candidate_cost = best_cost + 1
                if candidate_cost < cost[all_keys.index(near_valve)]:
                    cost[all_keys.index(near_valve)] = candidate_cost
        all_cost.append(deepcopy(cost))
    all_cost = np.array(all_cost)
    cost = [int(min(all_cost[:, k])) for k in range(len(cost))]
    return dict(zip(all_keys, cost))


def find_best(inputs, part):
    """
    return best flow with valves of inputs
    """
    valves = parse_input(inputs)
    meaningful = {key: value for key, value in valves.items() if value[0] != 0}
    distances = {key: dijkstra(valves, key) for key in list(meaningful.keys())}
    distances.update({"AA": dijkstra(valves, "AA")})
    encoded_valves = {valve: 1 << i for i, valve in enumerate(meaningful)}

    def process_case(last_valve, time_remaining, state, flow, answer):
        answer[state] = max(answer.get(state, 0), flow)
        for valve in meaningful:
            minutes = time_remaining - distances[last_valve][valve] - 1
            if (encoded_valves[valve] & state) or (minutes <= 0):
                continue
            process_case(valve, minutes, state |
                         encoded_valves[valve],
                         flow + minutes*valves[valve][0], answer)
        return answer
    if part == 1:
        return max(process_case('AA', 30, 0, 0, {}).values())
    else:
        paths = process_case('AA', 26, 0, 0, {})
        return max([flow1 + flow2
                    for path1, flow1 in paths.items()
                    for path2, flow2 in paths.items()
                    if not path1 & path2])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {find_best(my_tests, 1)}")
    print(f"Answer test part2 : {find_best(my_tests, 2)}")

    print(f"Answer part1 : {find_best(my_input, 1)}")
    print(f"Answer part2 : {find_best(my_input, 2)}")
