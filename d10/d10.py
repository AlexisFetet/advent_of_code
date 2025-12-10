"""
This file contains a code attempt for advent of code day 10
"""

import functools
import math
import re
import os
import z3

def parse_line(line):
    leds = sum([(1 << index) for index, value in enumerate(line[1:line.index(']')]) if value == '#'])
    bits = line.index(']') - 1
    buttons = list(map(lambda x: list(map(int, x.group(1).split(','))), re.finditer(r"\(((?:,?[0-9]+)+)\)", line)))
    joltage = list(map(int, line[line.index('{') + 1:line.index('}')].split(',')))
    return leds, buttons, joltage, bits

def solve_p1(lines):
    count = 0
    for line in lines:
        leds, buttons, _, bits = parse_line(line)
        buttons = [sum(map(lambda x: 1 << x, button)) for button in buttons]
        solver = z3.Solver()
        z3_target = z3.BitVecVal(leds, bits)
        z3_eq = z3.BitVecVal(0, bits)
        z3_buttons = [z3.BitVecVal(value, bits) for value in buttons]
        z3_is_button_pressed = [z3.BitVec(f"button{index}", bits) for index in range(len(buttons))]
        for (button, is_button_pressed) in zip(z3_buttons, z3_is_button_pressed):
            solver.add(z3.Or(is_button_pressed == z3.BitVecVal(0, bits), is_button_pressed == z3.BitVecVal(-1, bits)))
            z3_eq = z3_eq ^ (button & is_button_pressed)
        solver.add(z3_target == z3.simplify(z3_eq))
        local_counts = []
        while solver.check() == z3.sat:
            model = solver.model()
            new_constraint = z3.BoolVal(False)
            for button in z3_is_button_pressed:
                new_constraint = z3.Or(new_constraint, button != model[button])
            solver.add(z3.BoolVal(True) == new_constraint)
            local_counts += [sum([model[button].as_long() != 0 for button in z3_is_button_pressed])]
        count += min(local_counts)
    return count

def solve_p2(lines):
    count = 0
    for line in lines:
        _, buttons, joltages, bits = parse_line(line)
        solver = z3.Solver()
        z3_target = [z3.IntVal(joltage) for joltage in joltages]
        z3_eq = [z3.IntVal(0) for _ in range(bits)]
        z3_button_pressed_count = [z3.Int(f"button{index}") for index in range(len(buttons))]
        for (button, button_pressed_count) in zip(buttons, z3_button_pressed_count):
            solver.add(button_pressed_count >= z3.IntVal(0))
            z3_eq = [(eq + button_pressed_count) if index in button else eq for index, eq in enumerate(z3_eq)]
        for (target, eq) in zip(z3_target, z3_eq):
            solver.add(target == z3.simplify(eq))
        local_counts = []
        while solver.check() == z3.sat:
            model = solver.model()
            new_constraint = z3.IntVal(0)
            for button_count in z3_button_pressed_count:
                new_constraint = new_constraint + button_count
            presses = sum([model[button_count].as_long() for button_count in z3_button_pressed_count])
            solver.add(new_constraint < presses)
            local_counts += [presses]
        count += min(local_counts)
    return count

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer exemple part1 : {solve_p1(my_tests)}")
    print(f"Answer part1 : {solve_p1(my_input)}")
    print(f"Answer exemple part2 : {solve_p2(my_tests)}")
    print(f"Answer part2 : {solve_p2(my_input)}")
