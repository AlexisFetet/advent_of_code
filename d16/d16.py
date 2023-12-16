"""
This file contains a code attempt for advent of code day 16
"""


import os


def interfere(char: str, direction: tuple[int, int]) -> list[tuple[int, int]]:
    match(char):
        case '.': return [direction]
        case '|': return [(1, 0), (-1, 0)] if direction[0] == 0 else [direction]
        case '-': return [(0, 1), (0, -1)] if direction[1] == 0 else [direction]
        case '/': return [(direction[1] * -1, direction[0] * -1)]
        case '\\': return [(direction[1], direction[0])]


def part1(lines, beam=[0, 0, 0, 1]):
    beams = [beam]
    known = {(beam[0], beam[1]): [(beam[2], beam[3])]}
    while len(beams) != 0:
        new_beams = []
        for beam in beams:
            new_directions = interfere(
                lines[beam[0]][beam[1]], (beam[2], beam[3]))
            for direction in new_directions:
                new_beam = [beam[0] + direction[0], beam[1] +
                            direction[1], direction[0], direction[1]]
                if 0 <= new_beam[0] < len(lines) and 0 <= new_beam[1] < len(lines[0]):
                    point = known.get((new_beam[0], new_beam[1]), None)
                    if point is not None:
                        if ((direction[0], direction[1])) not in point:
                            known[(new_beam[0], new_beam[1])].append(
                                (direction[0], direction[1]))
                            new_beams.append(new_beam)
                    else:
                        known[(new_beam[0], new_beam[1])] = [
                            (direction[0], direction[1])]
                        new_beams.append(new_beam)
        beams = new_beams
    return len(known)


def part2(lines):
    candidates = []
    for y in range(len(lines)):
        candidates.append([y, 0, 0, 1])
        candidates.append([y, len(lines[0]) - 1, 0, -1])
    for x in range(len(lines[0])):
        candidates.append([0, x, 1, 0])
        candidates.append([len(lines) - 1, x, -1, 0])
    return max(map(lambda x: part1(lines, x), candidates))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
