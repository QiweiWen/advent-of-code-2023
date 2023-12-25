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
MOVE_OPPOSITE = [down, right, up, left]


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


def simulate(grid, cycles):
    rocks = set([(i, j) for i in range(len(grid))
                 for j in range(len(grid[0])) if grid[i][j] == 'O'])

    for i in range(cycles):
        for dir in [NORTH, WEST, SOUTH, EAST]:
            rocks = next_positions(rocks, dir, grid)

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


TEST_GRID = \
    ["O....#....",
     "O.OO#....#",
     ".....##...",
     "OO.#O....O",
     ".O.....O#.",
     "O.#..O.#.#",
     "..O..#O..O",
     ".......O..",
     "#....###..",
     "#OO..#...."]


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    grid = TEST_GRID
    rocks = simulate(grid, 1000000)
    draw_grid(grid, rocks)
