import sys
import os
import re
import importlib


def parse_input(inf):
    result = []
    for line in inf:
        d, l, rgb = line.split()
        l = int(l)
        # (#70c710)
        regex = "\(#([a-f0-9]*)\)"
        if match := re.match(regex, rgb):
            rgb = int(f"0x{match.group(1)}", 16)
            result.append((d, l, rgb))
    return result


def make_loop(digs):
    loop = [(0, 0)]
    colours = dict()
    end = (0, 0)
    for d, l, rgb in digs:
        if d == 'R':
            def move(x, n): return (x[0], x[1] + n)
        elif d == 'L':
            def move(x, n): return (x[0], x[1] - n)
        elif d == 'U':
            def move(x, n): return (x[0] - n, x[1])
        elif d == 'D':
            def move(x, n): return (x[0] + n, x[1])

        stroke = [move(end, i + 1) for i in range(l)]
        loop += stroke
        end = stroke[-1]
        for s in stroke:
            colours[s] = rgb

    l_border = min(j for (i, j) in loop)
    u_border = min(i for (i, j) in loop)

    if l_border < 0:
        loop = [(i, j - l_border) for (i, j) in loop]

    if u_border < 0:
        loop = [(i - u_border, j) for (i, j) in loop]

    return loop


CROSS_ABOVE = 1
CROSS_BELOW = 2
CROSS_MIDDLE = 3


def cross_type(i, j, loop, prev, next):
    prev = loop[prev]
    next = loop[next]

    i_min, j_min = min((prev, next))
    i_max, j_max = max((prev, next))

    above = j_min == j and i_min < i
    below = j_max == j and i_max > i

    if above and below:
        return CROSS_MIDDLE

    if above:
        return CROSS_BELOW

    if below:
        return CROSS_ABOVE

    return None


def plot_path(loop, inside):
    r_border = max(j for (i, j) in loop)
    d_border = max(i for (i, j) in loop)

    for i in range(d_border + 2):
        for j in range(r_border + 2):
            if (i, j) in loop:
                print("#", end="")
            elif (i, j) in inside:
                print('@', end="")
            else:
                print(".", end="")
        print("")


def ray_cast(loop, r_border, prev_map, next_map, row):
    intersections = []
    for col in range(r_border + 2):
        iprev = prev_map.get((row, col))
        inext = next_map.get((row, col))

        in_loop = (row, col) in loop
        curr_cross_type = None if not in_loop else\
            cross_type(row, col, loop, iprev, inext)
        intersections.append((col, curr_cross_type))
    intersections = [x for x in intersections if x[1]]
    return intersections


DEBUG = False


def num_intersections(col, cast):
    global DEBUG
    try:
        ind = next(i for i, c in enumerate(cast) if cast[i][0] > col)
        last_cross = None
        ncrosses = 0
        for i in range(ind, len(cast)):
            if cast[i][1] == CROSS_MIDDLE:
                ncrosses += 1
                last_cross = None
            elif last_cross is not None:
                if last_cross != cast[i][1]:
                    ncrosses += 1
                last_cross = None
            else:
                last_cross = cast[i][1]

        return ncrosses
    except StopIteration:
        return 0


def count_inside(loop):
    prev_map = dict()
    next_map = dict()
    for ind in range(len(loop)):
        iprev = len(loop) - 1 if ind == 0 else ind - 1
        inext = 0 if ind == len(loop) - 1 else ind + 1
        prev_map[loop[ind]] = iprev
        next_map[loop[ind]] = inext

    r_border = max(j for (i, j) in loop)
    d_border = max(i for (i, j) in loop)

    inside = set()

    global DEBUG
    for row in range(d_border + 1):
        cast = ray_cast(loop, r_border, prev_map, next_map, row)
        for col in range(r_border):
            DEBUG = (row, col) == (5, 1) 
            if (row, col) not in loop:
                crosses = num_intersections(col, cast)
                if crosses % 2 == 1:
                    inside.add((row, col))

    return inside


if __name__ == "__main__":
    input = parse_input(sys.stdin)
    loop = make_loop(input)
    inside = count_inside(loop)
    plot_path(loop, inside)
    print(len(inside) + len(loop) - 1)
