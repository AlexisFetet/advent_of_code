"""
This file contains a code attempt for advent of code day 7
"""

import os
from queue import LifoQueue
from copy import deepcopy


def peek(self: LifoQueue):
    """
    peek at top element
    """
    elem = self.get()
    self.put(elem)
    return elem


LifoQueue.peek = peek


class File():
    """represents a file"""

    def __init__(self, byte_size, name) -> None:
        self.name = name
        self.byte_size = int(byte_size)


class Folder():
    """represents a folder"""

    def __init__(self, name) -> None:
        self.name = name
        self.byte_size = 0
        self.root_of = []

    def size(self):
        """return the cumulative size of the folder"""
        self.byte_size = sum([elem.byte_size for elem in self.root_of])

    def add(self, elem):
        """add a new element in the folder"""
        self.root_of.append(elem)


def build(commands: list):
    """build the file system"""
    command_queue = LifoQueue()
    commands.reverse()

    candidate_folders = []
    sum_light_folders = 0

    for command_line in commands:
        command_queue.put(command_line)

    def process_command(command_queue: LifoQueue[str]):
        """builds outter folder"""
        cd_command = command_queue.get()
        current_folder = Folder(cd_command[5:])
        command_queue.get()  # remove ls

        while (not command_queue.empty() and
               not command_queue.peek().startswith("$ cd")):

            elem = command_queue.get()
            if elem[0] != "d":
                current_folder.add(File(*elem.split()))

        while not command_queue.empty() and command_queue.peek() != "$ cd ..":
            current_folder.add(process_command(command_queue))

        if not command_queue.empty():
            command_queue.get()  # remove cd ..

        current_folder.size()
        candidate_folders.append(current_folder)
        if current_folder.byte_size < 100000:
            nonlocal sum_light_folders
            sum_light_folders += current_folder.byte_size

        return current_folder

    system = process_command(command_queue)

    candidate_folders = [folder for folder in candidate_folders
                         if 70000000 + folder.byte_size -
                         candidate_folders[-1].byte_size > 30000000]

    return (sum_light_folders,
            min(candidate_folders,
                key=lambda x: x.byte_size).byte_size,
            system)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    ans1 = build(deepcopy(my_tests))
    print(f"Answer part1 : {ans1[0]}")
    print(f"Answer part2 : {ans1[1]}")

    ans2 = build(deepcopy(my_input))
    print(f"Answer part1 : {ans2[0]}")
    print(f"Answer part2 : {ans2[1]}")
