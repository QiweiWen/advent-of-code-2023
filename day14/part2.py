import sys
import bisect
from part1 import parse_input


def up(i, j, steps=1):
    return (i - steps, j)


def down(i, j, steps=1):
    return (i + steps, j)


def left(i, j, steps=1):
    return (i, j - steps)


def right(i, j, steps=1):
    return (i, j + steps)


def inside(grid, i, j):
    return i >= 0 and j >= 0 and i < len(grid) and j < len(grid[0])


NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

MOVE_ALONG = [up, left, down, right]


def next_positions(rocks, dir, grid):
    next_rocks = set()
    along = MOVE_ALONG[dir]
    for i, j in rocks:
        steps = 0
        curr_i = i
        curr_j = j
        while inside(grid, curr_i, curr_j) and grid[curr_i][curr_j] != '#':
            if (curr_i, curr_j) not in rocks:
                steps += 1
            curr_i, curr_j = along(curr_i, curr_j, 1)

        next_rock = along(i, j, steps)
        next_rocks.add(next_rock)
    return next_rocks


def key(rocks):
    return "".join([(str(i) + str(j)) for (i, j) in sorted(rocks)])


def load(rocks, grid):
    return sum(len(grid) - i for (i, j) in rocks)


def simulate(grid, cycles):
    period = 0
    offset = 0
    rocks = set([(i, j) for i in range(len(grid))
                 for j in range(len(grid[0])) if grid[i][j] == 'O'])
    seen = {key(rocks): 0}
    loads = [load(rocks, grid)]

    for i in range(cycles):
        for dir in [NORTH, WEST, SOUTH, EAST]:
            rocks = next_positions(rocks, dir, grid)

        repr = key(rocks)
        if (last := seen.get(repr, None)) is not None:
            period = i + 1 - last
            offset = last
            break

        loads.append(load(rocks, grid))
        seen[repr] = i + 1

    return loads[offset + (cycles - offset) % period]


def draw_grid(grid, rocks):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '#':
                print('#', end="")
            elif (i, j) in rocks:
                print('O', end="")
            else:
                print('.', end="")
        print()


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    ld = simulate(grid, 1000000000)
    print(ld)
