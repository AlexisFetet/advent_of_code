"""
This file contains a code attempt for advent of code day 16
"""


import os


def hex2bin(value):
    """
    return bit representation from hex representation
    """
    result = "0b"
    for char in value[2:]:
        result += bin(int(char, 16))[2:].zfill(4)
    return result


def toint(value):
    """
    return an integer value from string or int
    """
    result = None
    try:
        result = int(value, 2)
    except TypeError:
        result = value
    return result


def evaluate_bits(packet, bits_to_evaluate):
    """
    return the bits_to_evaluate first bits and the leftover
    """
    return (packet[:bits_to_evaluate+2], "0b" + packet[bits_to_evaluate+2:])


def type0(packet):
    """
    process a type 0 packet
    """
    temp = default(packet)
    result = 0
    for elem in temp[0][0]:
        result += toint(elem)
    return ((result, temp[0][1]), temp[1])


def type1(packet):
    """
    process a type 1 packet
    """
    temp = default(packet)
    result = 1
    for elem in temp[0][0]:
        result *= toint(elem)
    return ((result, temp[0][1]), temp[1])


def type2(packet):
    """
    process a type 2 packet
    """
    temp = default(packet)
    return ((min(temp[0][0], key=toint), temp[0][1]), temp[1])


def type3(packet):
    """
    process a type 3 packet
    """
    temp = default(packet)
    return ((max(temp[0][0], key=toint), temp[0][1]), temp[1])


def sub_type4(packet):
    """
    get value in type 4 packet
    """
    last_, stripped = evaluate_bits(packet, 1)
    octet, stripped = evaluate_bits(stripped, 4)
    if toint(last_) == 0:
        return (octet[2:], stripped)
    else:
        temp = sub_type4(stripped)
        return (octet[2:] + temp[0], temp[1])


def type4(packet):
    """
    process a type 4 packet
    """
    temp = sub_type4(packet)
    return ((toint("0b" + temp[0]), temp[1]), 0)


def type5(packet):
    """
    process a type 5 packet
    """
    temp = default(packet)
    return (((1 if temp[0][0][0] > temp[0][0][1] else 0),
            temp[0][1]), temp[1])


def type6(packet):
    """
    process a type 6 packet
    """
    temp = default(packet)
    return (((1 if temp[0][0][0] < temp[0][0][1] else 0),
            temp[0][1]), temp[1])


def type7(packet):
    """
    process a type 7 packet
    """
    temp = default(packet)
    return (((1 if temp[0][0][0] == temp[0][0][1] else 0),
            temp[0][1]), temp[1])


def length_type_0(packet):
    """
    process a length id type 0 packet
    """
    length, stripped = evaluate_bits(packet, 15)
    length = toint(length)
    init = len(stripped) - 2
    result = []
    sum_version = 0
    while init - (len(stripped) - 2) < length:
        temp = packet_process(stripped)
        result.append(temp[0][0])
        stripped = temp[0][1]
        sum_version += temp[1]
    return ((result, stripped), sum_version)


def length_type_1(packet):
    """
    process a length id type 1 packet
    """
    packet_nb, stripped = evaluate_bits(packet, 11)
    packet_nb = toint(packet_nb)
    result = []
    sum_version = 0
    for _ in range(packet_nb):
        temp = packet_process(stripped)
        result.append(temp[0][0])
        stripped = temp[0][1]
        sum_version += temp[1]
    return ((result, stripped), sum_version)


TYPE_FUNCTIONS = {
    4: type4,
}

LENGTH_TYPE_ID = {
    0: length_type_0,
    1: length_type_1,
}


def default(packet):
    """
    process a non type 4 packet
    """
    length_type_id, stripped = evaluate_bits(packet, 1)
    func = LENGTH_TYPE_ID.get(toint(length_type_id))
    return func(stripped)


def packet_process(packet):
    """
    process a packet
    """
    version, stripped = evaluate_bits(packet, 3)
    type_id, stripped = evaluate_bits(stripped, 3)
    func = TYPE_FUNCTIONS.get(toint(type_id), default)
    temp = func(stripped)
    return (temp[0], toint(version) + temp[1])


def receive_packet(packet):
    """
    entry point to process a received packet
    """
    packetbin = hex2bin(packet)
    temp = packet_process(packetbin)
    return (temp[1], toint(temp[0][0]))


TYPE_FUNCTIONS = {
    0: type0,
    1: type1,
    2: type2,
    3: type3,
    4: type4,
    5: type5,
    6: type6,
    7: type7,
}


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]

    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        my_tests = file.read().splitlines()

    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        my_input = file.read().splitlines()

    my_tests = ["0x" + test for test in my_tests]
    for test in my_tests:
        print(f"Packet : {test}")
        ans = receive_packet(test)
        print(f"Answer part1 : {ans[0]}")
        print(f"Answer part2 : {ans[1]}")
        print("\"--------------------------\"")

    my_input = "0x" + my_input[0]
    ans = receive_packet(my_input)
    print(f"Answer part1 : {ans[0]}")
    print(f"Answer part2 : {ans[1]}")
