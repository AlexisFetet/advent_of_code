"""
This file contains a code attempt for advent of code day 17
"""


import os
from typing import Any


class cCoordinate():

    def __init__(self, x_: int, y_: int) -> None:
        self.x = x_
        self.y = y_

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class cBoard():

    def __init__(self) -> None:
        self.points_occupied = []
        self.max_height = 0


class cPiece():

    def __init__(self, ref_point_: cCoordinate) -> None:
        self.ref_point = ref_point_

    def push(self, direction: int, board: cBoard) -> None:
        self.ref_point.x += direction
        my_points = self.get_points()
        for point in my_points:
            if (point in board.points_occupied[:min(40, len(board.points_occupied))]) or (point.x < 0) or (point.x > 6):
                self.ref_point.x -= direction
                break

    def fall(self, board: cBoard) -> bool:
        self.ref_point.y -= 1
        my_points = self.get_points()
        result = False
        for point in my_points:
            point_in_list = (
                point in board.points_occupied[:min(40, len(board.points_occupied))])
            if point_in_list or (point.y == 0):
                result = True
                if point_in_list:
                    self.ref_point.y += 1
                points_to_fix = self.get_points()
                board.points_occupied = points_to_fix + board.points_occupied
                board.max_height = max(
                    board.points_occupied, key=lambda x: x.y).y
                break
        return result

    def get_points(self) -> list[cCoordinate]:
        raise NotImplementedError


class cLine(cPiece):

    def __init__(self, board_: cBoard) -> None:
        ref_point = cCoordinate(2, board_.max_height + 4)
        super().__init__(ref_point)

    def get_points(self) -> list[cCoordinate]:
        points = [
            self.ref_point,
            cCoordinate(self.ref_point.x + 1, self.ref_point.y),
            cCoordinate(self.ref_point.x + 2, self.ref_point.y),
            cCoordinate(self.ref_point.x + 3, self.ref_point.y),
        ]
        return points


class cCross(cPiece):

    def __init__(self, board_: cBoard) -> None:
        ref_point = cCoordinate(3, board_.max_height + 5)
        super().__init__(ref_point)

    def get_points(self) -> list[cCoordinate]:
        points = [
            self.ref_point,
            cCoordinate(self.ref_point.x + 1, self.ref_point.y),
            cCoordinate(self.ref_point.x - 1, self.ref_point.y),
            cCoordinate(self.ref_point.x, self.ref_point.y + 1),
            cCoordinate(self.ref_point.x, self.ref_point.y - 1),
        ]
        return points


class cCorner(cPiece):

    def __init__(self, board_: cBoard) -> None:
        ref_point = cCoordinate(2, board_.max_height + 4)
        super().__init__(ref_point)

    def get_points(self) -> list[cCoordinate]:
        points = [
            self.ref_point,
            cCoordinate(self.ref_point.x + 1, self.ref_point.y),
            cCoordinate(self.ref_point.x + 2, self.ref_point.y),
            cCoordinate(self.ref_point.x + 2, self.ref_point.y + 1),
            cCoordinate(self.ref_point.x + 2, self.ref_point.y + 2),
        ]
        return points


class cVLine(cPiece):

    def __init__(self, board_: cBoard) -> None:
        ref_point = cCoordinate(2, board_.max_height + 4)
        super().__init__(ref_point)

    def get_points(self) -> list[cCoordinate]:
        points = [
            self.ref_point,
            cCoordinate(self.ref_point.x, self.ref_point.y + 1),
            cCoordinate(self.ref_point.x, self.ref_point.y + 2),
            cCoordinate(self.ref_point.x, self.ref_point.y + 3),
        ]
        return points


class cSquare(cPiece):

    def __init__(self, board_: cBoard) -> None:
        ref_point = cCoordinate(2, board_.max_height + 4)
        super().__init__(ref_point)

    def get_points(self) -> list[cCoordinate]:
        points = [
            self.ref_point,
            cCoordinate(self.ref_point.x, self.ref_point.y + 1),
            cCoordinate(self.ref_point.x + 1, self.ref_point.y),
            cCoordinate(self.ref_point.x + 1, self.ref_point.y + 1),
        ]
        return points


INSTANCIATION_SEQUENCE = [cLine, cCross, cCorner, cVLine, cSquare]


def get_direction(flow):
    result = None
    if '>' == flow:
        result = 1
    elif '<' == flow:
        result = -1
    return result


def part1(flow: str, max_stones: int, answers=None):
    flow_index = -1
    instanciation_index = 0
    used_pieces = 0
    board = cBoard()
    if answers != None:
        max_stones = len(answers) - 1
    while used_pieces < max_stones:
        used_pieces += 1
        new_piece = INSTANCIATION_SEQUENCE[instanciation_index](board)
        instanciation_index = (instanciation_index +
                               1) % len(INSTANCIATION_SEQUENCE)
        flow_index = (flow_index + 1) % len(flow)
        new_piece.push(get_direction(flow[flow_index]), board)
        while not new_piece.fall(board):
            flow_index = (flow_index + 1) % len(flow)
            new_piece.push(get_direction(flow[flow_index]), board)
        if answers is not None:
            print(f"Done with {used_pieces}")
            if (int(answers[used_pieces]) != (board.max_height + 1)):
                raise Exception(
                    f"Erreur at {used_pieces} : got {board.max_height + 1} expected {answers[used_pieces]}")

    # board_lines = []
    # for _ in range(board.max_height + 1):
    #     board_lines.append([".", ".", ".", ".", ".", ".", "."])
    # for point in board.points_occupied:
    #     board_lines[point.y][point.x] = '#'
    # board_lines.reverse()
    # for line in board_lines:
    #     print(line)

    return board.max_height + 1


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    # part1(my_tests[0], 2022, my_tests[1:])

    print(f"Answer part1 : {part1(my_input[0], 2022)}")
    print(f"Answer part2 : {0}")
