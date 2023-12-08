import sys
from part1 import solve


def parse_input(lines):
    times = lines[0].split(":")[1].split()
    dists = lines[1].split(":")[1].split()
    time = int("".join(times))
    dist = int("".join(dists))
    return time, dist


if __name__ == "__main__":
    time, dist = parse_input([x for x in sys.stdin])
    print(solve(time, dist))
