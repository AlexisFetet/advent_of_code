"""
This file contains a code attempt for advent of code day 11
"""


import os
from typing import Union


def generate_operation(operation_str: str):
    """
    generate operation for monkey
    """
    operation_str = operation_str.split()

    def operation(old: int):
        first = old if operation_str[2] == "old" else int(operation_str[2])
        second = old if operation_str[4] == "old" else int(operation_str[4])
        return first + second if operation_str[3] == "+" else first * second

    return operation


class Monkey():
    """
    represents a monkey
    """

    def __init__(self,
                 monkey_id: int,
                 items: list[int],
                 operation_str: str,
                 test: int,
                 true_monkey: int,
                 false_monkey: int) -> None:
        self.monkey_id = monkey_id
        self.items = items
        self.test = test
        self.operation = generate_operation(operation_str)
        self.true_monkey: Union[int, Monkey] = true_monkey
        self.false_monkey: Union[int, Monkey] = false_monkey
        self.examinated = 0
        self.reduce = None

    def link(self, monkey_list: list['Monkey']):
        """
        link monkeys
        """
        self.false_monkey = monkey_list[self.false_monkey]
        self.true_monkey = monkey_list[self.true_monkey]

    def examinate(self):
        """
        examinate 1 item
        """
        self.examinated += 1
        new = self.reduce(self.operation(self.items.pop()))
        if new % self.test == 0:
            self.true_monkey.receive(new)
        else:
            self.false_monkey.receive(new)

    def examinate_all(self):
        """
        examinate all available items
        """
        while len(self.items) != 0:
            self.examinate()

    def receive(self, item):
        """
        receive items from other monkeys
        """
        self.items.append(item)

    def def_reduction(self, reduce):
        """
        define reducer
        """
        self.reduce = reduce


def run_monkeys(input_list, part):
    """
    process the problem
    """
    divider = 1
    monkeys: list[Monkey] = []
    monkey_nb = len(input_list) // 7
    for _id in range(monkey_nb + 1):
        _items = [int(x.strip()) for x in input_list[_id*7+1][17:].split(",")]
        _operation = input_list[_id*7+2][13:]
        _test = int(input_list[_id*7+3][20:])
        _true_monkey = int(input_list[_id*7+4][28:])
        _false_monkey = int(input_list[_id*7+5][29:])
        monkeys.append(Monkey(_id,
                              _items,
                              _operation,
                              _test,
                              _true_monkey,
                              _false_monkey))
        divider *= _test

    for monkey in monkeys:
        monkey.link(monkeys)
        monkey.def_reduction((lambda x: x // 3)
                             if part == 1
                             else (lambda x: x % divider))

    for _ in range(20 if part == 1 else 10000):
        for monkey in monkeys:
            monkey.examinate_all()

    examinated = [monkey.examinated for monkey in monkeys]
    examinated.sort()
    return examinated[-1]*examinated[-2]


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {run_monkeys(my_tests, 1)}")
    print(f"Answer test part2 : {run_monkeys(my_tests, 2)}")

    print(f"Answer part1 : {run_monkeys(my_input, 1)}")
    print(f"Answer part2 : {run_monkeys(my_input, 2)}")
