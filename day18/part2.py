import sys
from part1 import *


def input_to_digs(input):
    return [(rgb & 0xf, rgb >> 4, rgb) for _, _, rgb in input]


if __name__ == "__main__":
    digs = input_to_digs(parse_input(sys.stdin))
    loop, perim = make_loop(digs)
    print(loop_area(loop, perim))
