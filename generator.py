import os

for k in range(1, 26):
    day = "d%02d" % k
    os.mkdir(day)
    with open(day + "/" + day + ".txt", "a+", encoding="utf-8"):
        pass
    with open(day + "/" + day + "_tests_input.txt", "a+", encoding="utf-8"):
        pass
    sample = """\"\"\"
This file contains a code attempt for advent of code day %i
\"\"\"


import os

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    print(f"Answer part1 : {0}")
    print(f"Answer part2 : {0}")
""" % k
    with open(day + "/" + day + ".py", "a+", encoding="utf-8") as file:
        file.write(sample)
