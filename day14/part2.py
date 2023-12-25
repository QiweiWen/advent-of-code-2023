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


def how_far(grid, move, i, j):
    target = (i, j)
    while inside(grid, i, j) and grid[i][j] != '#':
        target = (i, j)
        i, j = move(i, j, 1)
    return target


def build_cache(grid):
    cache = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # how far can grid[i][j] roll in each direction, NWSE?
            north = how_far(grid, up, i, j)
            west = how_far(grid, left, i, j)
            south = how_far(grid, down, i, j)
            east = how_far(grid, right, i, j)
            cache[(i, j)] = (north, west, south, east)
    return cache


NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

MOVE_IN_SAME_DIR = [up, left, down, right]
MOVE_IN_OPPOSITE_DIR = [down, right, up, left]


def next_positions(rocks, dir, cache):
    next_rocks = []
    for i, j in rocks:
        bottom = cache[(i, j)][dir]
        bisect.insort(next_rocks, bottom)

    move = MOVE_IN_OPPOSITE_DIR[dir]
    # compensate now that all the rocks have been stacked to the bottom
    last = None
    stack_height = 1
    for idx in range(len(next_rocks)):
        curr = next_rocks[idx]
        if curr == last:
            move_i, move_j = move(curr[0], curr[1], stack_height)
            next_rocks[idx] = (move_i, move_j)
            stack_height += 1
            continue

        if not last:
            last = curr
            continue

        stack_height = 1
        last = curr

    return next_rocks


def simulate(grid, cycles):
    cache = build_cache(grid)
    rocks = [(i, j) for i in range(len(grid))
             for j in range(len(grid[0])) if grid[i][j] == 'O']

    for i in range(cycles):
        for dir in [NORTH, WEST, SOUTH, EAST]:
            rocks = next_positions(rocks, dir, cache)
        
        if (i + 1) % 10000 == 0:
            print(f"Simulated {i + 1} iterations")

    return rocks


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
    rocks = simulate(grid, 1000000)
    print("After 1,000,000 cycles:")
    draw_grid(grid, rocks)
    print()
