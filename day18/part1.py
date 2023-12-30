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
    loop = {(0, 0): None}
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
        for s in stroke:
            loop[s] = rgb
        end = stroke[-1]

    l_border = min(j for (i, j) in loop)
    u_border = min(i for (i, j) in loop)

    if l_border < 0:
        loop = [(i, j - l_border) for (i, j) in loop]

    if u_border < 0:
        loop = [(i - u_border, j) for (i, j) in loop]

    return loop


NOT_CROSSED = 0
CROSSING = 1

CROSS_ABOVE = 0
CROSS_BELOW = 1
CROSS_MIDDLE = 2

def is_inside(loop, r_border, i, j):
    state = NOT_CROSSED

    ncross = 0
    while j <= r_border + 1:
        if state == NOT_CROSSED:
            if (i, j) in loop:
                state = CROSSING
        elif state == CROSSING:
            if (i, j) not in loop:
                state = NOT_CROSSED
                ncross += 1
        j += 1
    return ncross % 2 == 1


def plot_path(loop):
    r_border = max(j for (i, j) in loop)
    d_border = max(i for (i, j) in loop)

    for i in range(d_border + 2):
        for j in range(r_border + 2):
            if (i, j) in loop:
                print("#", end="")
            elif is_inside(loop, r_border, i, j):
                print('@', end="")
            else:
                print(".", end="")
        print("")


if __name__ == "__main__":
    input = parse_input(sys.stdin)
    loop = make_loop(input)
    plot_path(loop)
