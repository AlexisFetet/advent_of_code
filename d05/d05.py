"""
This file contains a code attempt for advent of code day 5
"""

import re
import os

NUMBER_REGEX = re.compile(r"([0-9]+)")
TABLE_REGEX = re.compile(r"([a-z]+)-to-([a-z]+) map:\n((?:(?:[0-9]+)\s(?:[0-9]+)\s(?:[0-9]+)\n)+)")


def convert(indx, table):
    result = indx
    for line in table:
        if line[1] <= indx < (line[1] + line[2]):
            result = line[0] + (indx - line[1])
            break
    return result

def convert2(start, width, table):
    ranges_to_convert = [(start, width)]
    converted_ranges = []
    for (destination_start, source_start, source_range) in table:
        indexes_to_pop = []
        ranges_to_insert = []
        for indx, (candidate_start, candidate_range) in enumerate(ranges_to_convert):
            if (candidate_start < source_start + source_range and source_start < candidate_start + candidate_range):

                intersect_start = max(candidate_start, source_start)
                intersect_end = min(candidate_start + candidate_range, source_start + source_range)

                converted_range_start = destination_start + (intersect_start - source_start)
                converted_range_width = intersect_end - intersect_start
                converted_ranges.append((converted_range_start, converted_range_width))

                if(candidate_start < source_start):
                    ranges_to_insert.append((candidate_start, source_start - candidate_start))

                if(source_start + source_range < candidate_start + candidate_range):
                    ranges_to_insert.append((source_start + source_range, (candidate_start + candidate_range) - (source_start + source_range)))

                indexes_to_pop.append(indx)

        for indx in indexes_to_pop:
            ranges_to_convert.pop(indx)
        ranges_to_convert += ranges_to_insert

    converted_ranges += ranges_to_convert
        
    return converted_ranges



def part1(lines):
    tables = [list(zip(*[iter([int(x) for x in NUMBER_REGEX.findall(table[2])])]*3)) for table in TABLE_REGEX.findall("\n".join(lines))]
    seeds = [int(x) for x in NUMBER_REGEX.findall(lines[0])]
    for table in tables:
        seeds = [convert(seed, table) for seed in seeds]
    return min(seeds)

def part2(lines):
    tables = [list(zip(*[iter([int(x) for x in NUMBER_REGEX.findall(table[2])])]*3)) for table in TABLE_REGEX.findall("\n".join(lines))]
    seeds = list(zip(*[iter([int(x) for x in NUMBER_REGEX.findall(lines[0])])]*2))
    for table in tables:
        temp = []
        for seed in seeds:
            temp += convert2(seed[0], seed[1], table)
        seeds = temp
    return min(seeds, key=lambda x: x[0])[0]

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {part1(my_input)}")
    print(f"Answer part2 : {part2(my_input)}")
