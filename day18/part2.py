import sys
from part1 import parse_input

R = 0
D = 1
L = 2
U = 3

def input_to_digs(input):
    return [(rgb & 0xf, rgb >> 4) for _, _, rgb in input]


if __name__ == "__main__":
    input = parse_input(sys.stdin)