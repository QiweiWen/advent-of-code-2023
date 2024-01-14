import sys
import re


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


R = 0
D = 1
L = 2
U = 3


def make_loop(digs):
    perimeter = 0
    loop = [(0, 0)]
    end = (0, 0)
    for d, l, rgb in digs:
        if d in ['R', R]:
            def move(x, n): return (x[0], x[1] + n)
        elif d in ['L', L]:
            def move(x, n): return (x[0], x[1] - n)
        elif d in ['U', U]:
            def move(x, n): return (x[0] - n, x[1])
        elif d in ['D', D]:
            def move(x, n): return (x[0] + n, x[1])

        perimeter += l
        vertex = move(end, l)
        loop.append(vertex)
        end = vertex

    l_border = min(j for (i, j) in loop)
    u_border = min(i for (i, j) in loop)

    if l_border < 0:
        loop = [(i, j - l_border) for (i, j) in loop]

    if u_border < 0:
        loop = [(i - u_border, j) for (i, j) in loop]

    return loop, perimeter


def loop_area(loop, perimeter):
    total_area = 0
    for i in range(len(loop) - 1):
        x1, y1 = loop[i]
        x2, y2 = loop[i + 1]
        subarea = (y2 + y1) * (x2 - x1)
        total_area += subarea

    # https://www.reddit.com/r/adventofcode/comments/18l8mao/2023_day_18_intuition_for_why_spoiler_alone/
    return abs(total_area // 2) + perimeter // 2 + 1


def in_loop(loop, row, col):
    for i in range(len(loop) - 1):
        v1 = loop[i]
        v2 = loop[i + 1]
        r1, c1 = min(v1, v2)
        r2, c2 = max(v1, v2)

        if r1 == row and r2 == row and c1 <= col and col <= c2:
            return True
        if c1 == col and c2 == col and r1 <= row and row <= r2:
            return True
    return False


def plot_path(loop):
    r_border = max(j for (i, j) in loop)
    d_border = max(i for (i, j) in loop)

    for i in range(d_border + 2):
        for j in range(r_border + 2):
            if in_loop(loop, i, j):
                print("#", end="")
            else:
                print(".", end="")
        print("")


if __name__ == "__main__":
    input = parse_input(sys.stdin)
    loop, perim = make_loop(input)
    # plot_path(loop)
    print(loop_area(loop, perim))
