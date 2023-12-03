import sys
from part1 import decode


def power(decoded):
    if not decoded:
        return 0
    return max(decoded["red"]) * max(decoded["blue"]) * max(decoded["green"])


if __name__ == "__main__":
    print(sum(power(decode(x)) for x in sys.stdin))
