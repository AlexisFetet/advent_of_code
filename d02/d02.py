"""
This file contains a code attempt for advent of code day 2
"""


import os


class SubMarine():
    """
    class representing a submarine for question 1
    """

    def __init__(self) -> None:
        self.depth = 0
        self.location = 0
        self.aim = 0

    def down_move(self, val):
        """
        proceed with down order with value val
        """
        self.depth += val

    def up_move(self, val):
        """
        proceed with down order with value val
        """
        self.depth -= val

    def forward_move(self, val):
        """
        proceed with forward order with value val
        """
        self.location += val

    ORDER = {
        "up": up_move,
        "down": down_move,
        "forward": forward_move,
    }

    def process_order(self, order):
        """
        process a tuple(order, value)
        """
        func = self.ORDER.get(order[0])
        func(self, int(order[1]))

    def process_orders(self, order_list):
        """
        process an order list
        """
        for order in order_list:
            self.process_order(order)


class SubMarine2(SubMarine):
    """
    class representing a submarine for question 2
    """

    def down_move(self, val):
        self.aim += val

    def up_move(self, val):
        self.aim -= val

    def forward_move(self, val):
        self.location += val
        self.depth += val*self.aim

    ORDER = {
        "up": up_move,
        "down": down_move,
        "forward": forward_move,
    }


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [order.split() for order in my_tests]
    my_input = [order.split() for order in my_input]

    my_test_submarine = SubMarine()
    my_test_submarine.process_orders(my_tests)
    print(f"Answer part1 : "
          f"{my_test_submarine.depth*my_test_submarine.location}")
    my_test_submarine2 = SubMarine2()
    my_test_submarine2.process_orders(my_tests)
    print(f"Answer part2 : "
          f"{my_test_submarine2.depth*my_test_submarine2.location}")

    my_submarine = SubMarine()
    my_submarine.process_orders(my_input)
    print(f"Answer part1 : {my_submarine.depth*my_submarine.location}")
    my_submarine2 = SubMarine2()
    my_submarine2.process_orders(my_input)
    print(f"Answer part2 : {my_submarine2.depth*my_submarine2.location}")
