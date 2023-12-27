from part1 import *
import sys


def starting_positions(grid):
    positions = []
    for j in range(len(grid[0])):
        positions.append(((0, j), DOWN))

    for j in range(len(grid[-1])):
        i = len(grid) - 1
        positions.append(((i, j), UP))

    for i in range(0, len(grid)):
        positions.append(((i, 0), RIGHT))
        j = len(grid[i]) - 1
        positions.append(((i, j), LEFT))
    return positions


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    positions = starting_positions(grid)
    num_energised = [len(energise(grid, pos)) for pos in positions]
    print(max(num_energised))
