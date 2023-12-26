import sys


def parse_input(inf):
    return inf.read().strip().split(",")


def encode(string):
    enc = 0
    for s in string:
        enc += ord(s)
        enc = enc * 17
        enc = enc % 256
    return enc


if __name__ == "__main__":
    strings = parse_input(sys.stdin)
    print(sum(encode(s) for s in strings))
