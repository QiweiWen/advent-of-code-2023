import sys
from enum import Enum
from part1 import *


def draw_loop(grid, loop, inside):
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            if (x, y) in loop:
                print(f"\033[92m{grid[y][x]}\033[0m", end="")
            elif (x, y) in inside:
                print(f"\033[93m{grid[y][x]}\033[0m", end="")
            else:
                print((grid[y][x]), end="")
        print()


def direction(xf, yf, xt, yt):
    if xf == xt:
        return Direction.Up if yt < yf else Direction.Down
    if yf == yt:
        return Direction.Left if xt < xf else Direction.Right


def replace_S(grid, loop):
    sidx = next(s for s, (x, y) in enumerate(loop) if grid[y][x] == 'S')

    predecessor = len(loop) - 1 if sidx == 0 else sidx - 1
    successor = 0 if sidx == len(loop) - 1 else sidx + 1

    xa, ya = loop[sidx]
    xp, yp = loop[predecessor]
    xs, ys = loop[successor]

    dirs = set([direction(xp, yp, xa, ya), direction(xs, ys, xa, ya)])
    token = next(t for (t, v) in g_token_direction_map.items()
                 if set(v) == dirs)
    grid[ya][xa] = token


def is_inside(grid, loop, x, y):
    if (x, y) in loop:
        return False
    ray_cast = ((xr, y) for xr in range(x + 1, len(grid[0])))
    intersects = [(x, y) for (x, y) in ray_cast
                  if (x, y) in loop and grid[y][x] in "|LJ7F"]
    intersects = "".join(grid[y][x] for (x, y) in intersects)
    intersects = intersects.replace("LJ", "")
    intersects = intersects.replace("L7", "-")
    intersects = intersects.replace("FJ", "-")
    intersects = intersects.replace("F7", "")
    return len(intersects) % 2 != 0


def count_enclosed(grid):
    loop = find_main_loop(grid)
    replace_S(grid, loop)

    #is_inside(grid, loop, 4, 4)
    #return 0
    inside = []
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            if (x, y) in loop:
                continue

            if is_inside(grid, loop, x, y):
                inside.append((x, y))

    draw_loop(grid, loop, inside)
    return len(inside)


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    print(count_enclosed(grid))
