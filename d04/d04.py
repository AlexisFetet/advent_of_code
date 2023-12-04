"""
This file contains a code attempt for advent of code day 4
"""


import os


def overlaps(sections):
    """
    return true if a group is included in the other
    """
    section1 = range(int(sections[0][0]), int(sections[0][1])+1)
    section2 = range(int(sections[1][0]), int(sections[1][1])+1)
    return (all(section in section1 for section in section2)
            or all(section in section2 for section in section1))


def overlap_by(sections):
    """
    return true if groups have overlapping sections
    """
    section1 = range(int(sections[0][0]), int(sections[0][1])+1)
    section2 = range(int(sections[1][0]), int(sections[1][1])+1)
    return any(section in section1 for section in section2)


def count_overlaping(sections_list):
    """
    count how many section groups have a group including the other
    """
    return sum([overlaps(sections) for sections in sections_list])


def count_overlaping_sections(sections_list):
    """
    count how many sections group have overlapping sections
    """
    return sum([overlap_by(sections) for sections in sections_list])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = [[entry.split("-") for entry in section.split(",")]
                for section in my_tests]
    my_input = [[entry.split("-") for entry in section.split(",")]
                for section in my_input]

    print(f"Answer test part1 : {count_overlaping(my_tests)}")
    print(f"Answer test part2 : {count_overlaping_sections(my_tests)}")

    print(f"Answer part1 : {count_overlaping(my_input)}")
    print(f"Answer part2 : {count_overlaping_sections(my_input)}")
