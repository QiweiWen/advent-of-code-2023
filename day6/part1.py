import sys
import math


def parse_input(lines):
    times = lines[0].split(":")[1].split()
    dists = lines[1].split(":")[1].split()
    times = [int(x) for x in times]
    dists = [int(x) for x in dists]
    return times, dists


def solve(time, min_dist):
    # (T - x) * x - min_dist == 0
    # -x^2 + Tx - min_dist == 0
    b2min4ac = time * time - 4 * min_dist
    if b2min4ac <= 0:
        return 0

    xmin = ((-1 * time) + math.sqrt(b2min4ac)) / -2
    xmax = ((-1 * time) - math.sqrt(b2min4ac)) / -2

    lower = math.ceil(xmin)
    upper = math.floor(xmax)

    lower = lower if lower != xmin else lower + 1
    upper = upper if upper != xmax else upper - 1

    if upper < 0:
        return 0

    lower = max(0, lower)
    return upper - lower + 1


if __name__ == "__main__":
    time, dist = parse_input([x for x in sys.stdin])
    solutions = [solve(time[i], dist[i]) for i in range(len(time))]
    print(math.prod(solutions))
