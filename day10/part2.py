import sys
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


def winding_number(grid, loop, x, y):
    right_intersect = None
    loop_idx_map = {(x, y): idx for idx, (x, y) in enumerate(loop)}
    for xr in range(x + 1, len(grid[0])):
        right_intersect = loop_idx_map.get((xr, y))
        if right_intersect:
            break

    if not right_intersect:
        return 0

    wind_angle = 0
    start_idx = right_intersect
    loop_idx = start_idx
    for i in range(1, len(loop) + 1):
        last_idx = loop_idx
        loop_idx = (start_idx + i) % len(loop)
        xt, yt = loop[loop_idx]
        xf, yf = loop[last_idx]
        dir = direction(xf, yf, xt, yt)

        token = grid[yt][xt]
        if token == 'L':
            assert (dir == Direction.Left or dir == Direction.Down)
            if dir == Direction.Left:
                wind_angle -= 90
            elif dir == Direction.Down:
                wind_angle += 90
        if token == 'J':
            assert (dir == Direction.Down or dir == Direction.Right)
            if dir == Direction.Down:
                wind_angle -= 90
            elif dir == Direction.Right:
                wind_angle += 90
        if token == '7':
            assert (dir == Direction.Right or dir == Direction.Up)
            if dir == Direction.Right:
                wind_angle -= 90
            elif dir == Direction.Up:
                wind_angle += 90
        if token == 'F':
            assert (dir == Direction.Left or dir == Direction.Up)
            if dir == Direction.Up:
                wind_angle -= 90
            elif dir == Direction.Left:
                wind_angle += 90

    return wind_angle != 0


def count_enclosed(grid):
    loop = find_main_loop(grid)
    draw_loop(grid, loop, [])
    print(winding_number(grid, loop, 0, 1))
    return 0
    inside = []
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            if (x, y) in loop:
                continue

            if winding_number(grid, loop, x, y) != 0:
                inside.append((x, y))

    draw_loop(grid, loop, inside)
    return len(inside)


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    print(count_enclosed(grid))
