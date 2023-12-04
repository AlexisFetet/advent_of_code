"""
This file contains a code attempt for advent of code day 15
"""


import os
import re
import time

COORDINATES = re.compile(r"x=(-*[0-9]*),\sy=(-*[0-9]*)")


class Sensor():
    """
    represents a sensor
    """

    def __init__(self,
                 coord_x,
                 coord_y,
                 coord_beacon_x,
                 coord_beacon_y) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.closest_beacon = (abs(coord_x - coord_beacon_x) +
                               abs(coord_y - coord_beacon_y))

    def admit(self, coord_x, coord_y):
        """
        return true if beacon at (coord_x, coord_y) is further than
        the closest declared beacon
        """
        return ((abs(self.coord_x - coord_x) + abs(self.coord_y - coord_y))
                > self.closest_beacon)

    def border(self):
        """
        return all positions at distance closest_beacon + 1
        """
        positions = []
        for iter_ in range(self.closest_beacon + 1):
            offset = iter_
            positions.append((self.coord_x - self.closest_beacon - 1 + offset,
                              self.coord_y - offset))
            positions.append((self.coord_x + offset,
                              self.coord_y - self.closest_beacon - 1 + offset))
            positions.append((self.coord_x + self.closest_beacon + 1 - offset,
                              self.coord_y + offset))
            positions.append((self.coord_x - offset,
                              self.coord_y + self.closest_beacon + 1 - offset))
        return positions

    def __repr__(self) -> str:
        return f"Sensor at {self.coord_x, self.coord_y} with closest at {self.closest_beacon}"

def count_possible(sensors: list[Sensor],
                   beacon_list: list[tuple[int, int]],
                   line):
    """
    count the amount of possible locations for an undetected beacon at line
    """
    occupied = set()

    for sensor in sensors:
        offset = abs(sensor.coord_y - line)
        for x in range(sensor.coord_x - sensor.closest_beacon + offset,
                       sensor.coord_x + sensor.closest_beacon - offset + 1):
            if (x, line) not in beacon_list:
                occupied.add((x, line))
    return len(occupied)


def search(sensors: list[Sensor],
           beacon_list: list[tuple[int, int]],
           max_coord):
    """
    return the frequency of the detress beacon
    """
    candidates = []
    for sensor in sensors:
        candidates += sensor.border()
    for candidate in candidates:
        if 0 <= candidate[0] <= max_coord and 0 <= candidate[1] <= max_coord:
            result = True
            for sensor in sensors:
                if not sensor.admit(*candidate):
                    result = False
                    break
            if result:
                return candidate[0] * 4000000 + candidate[1]
    return 0


def generate_sensor_list(sensors):
    """
    generate sensor list from an input
    """
    sensor_list: list[Sensor] = []
    beacon_list: list[tuple[int, int]] = []
    for sensor in sensors:
        [[sensor_x, sensor_y],
         [beacon_x, beacon_y]] = COORDINATES.findall(sensor)
        sensor_list.append(Sensor(int(sensor_x),
                                  int(sensor_y),
                                  int(beacon_x),
                                  int(beacon_y)))
        beacon_list.append((int(beacon_x), int(beacon_y)))
    return (sensor_list,
            beacon_list)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    result_test = count_possible(*generate_sensor_list(my_tests), 10)
    print(f"Answer part1 : {result_test}")
    print(f"Answer test part2 : {search(*generate_sensor_list(my_tests), 20)}")

    result_input = count_possible(*generate_sensor_list(my_input), 2000000)
    print(f"Answer part1 : {result_input}")
    print(f"Answer part2 : {search(*generate_sensor_list(my_input), 4000000)}")
