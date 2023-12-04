"""
This file contains a code attempt for advent of code day 10
"""


import os


def process(commands):
    """
    process commands
    """
    total = 0
    register = 1
    cycle = 1
    render = ""
    sprite = [0, 1, 2]

    def tick(register, sprite):
        nonlocal total, render, cycle
        current = (cycle-1) % 40
        if current == 0:
            render += "\n"
        if current in sprite:
            render += "#"
        else:
            render += "."
        if cycle % 40 == 20:
            total += cycle*register
        cycle += 1

    for command in commands:
        tick(register, sprite)
        if command[0] == "noop":
            continue
        if command[0] == "addx":
            tick(register, sprite)
            register += int(command[1])
            sprite = [register-1, register, register+1]
            continue
    return total, (render + "\n")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [command.split() for command in my_tests]
    my_input = [command.split() for command in my_input]

    total_test, render_test = process(my_tests)
    print(f"Answer test part1 : {total_test}")
    print("Answer test part2 : ")
    print(render_test)

    total_input, render_input = process(my_input)
    print(f"Answer part1 : {total_input}")
    print("Answer part2 : ")
    print(render_input)
