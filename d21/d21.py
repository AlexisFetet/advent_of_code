"""
This file contains a code attempt for advent of code day 21
"""


import os
import sympy


def create_equation(lines):
    """
    generate equation from lines
    """
    gen_dict = {}
    for line in lines:
        temp = line.split(": ")
        gen_dict.update({temp[0]: temp[1]})
    return int(eval(recur("root", gen_dict)))


def recur(expr, dict_):
    """
    recursively build expression
    """
    expression = dict_[expr]
    expression = expression.split()
    if len(expression) == 1:
        return expression[0]
    else:
        return str("(" + (recur(expression[0], dict_) +
                          expression[1] +
                          recur(expression[2], dict_) + ")"))


def create_equation2(lines):
    """
    generate equation from lines
    """
    gen_dict = {}
    for line in lines:
        temp = line.split(": ")
        gen_dict.update({temp[0]: temp[1]})
    exprs = gen_dict["root"].split()
    expr1 = recur2(exprs[0], gen_dict)
    expr2 = recur2(exprs[2], gen_dict)
    humn = sympy.symbols('humn')
    return sympy.solve(expr2 + "-" + expr1, humn)[0]


def recur2(expr, dict_):
    """
    recursively build expression
    """
    expression = dict_[expr]
    expression = expression.split()
    if expr == "humn":
        return expr
    if len(expression) == 1:
        return expression[0]
    else:
        return str("(" + (recur2(expression[0], dict_) +
                          expression[1] +
                          recur2(expression[2], dict_) + ")"))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer test part1 : {create_equation(my_tests)}")
    print(f"Answer test part2 : {create_equation2(my_tests)}")

    print(f"Answer part1 : {create_equation(my_input)}")
    print(f"Answer part2 : {create_equation2(my_input)}")
