import sys
from enum import Enum


class Pipe(Enum):
    NS = '|'
    EW = '-'
    NE = 'L'
    NW = 'J'
    SW = '7'
    SE = 'F'
    GN = '.'
    ANIMAL = 'S'


class Direction(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3


def complement(dir):
    if dir == Direction.Up:
        return Direction.Down
    if dir == Direction.Down:
        return Direction.Up
    if dir == Direction.Left:
        return Direction.Right
    if dir == Direction.Right:
        return Direction.Left


g_token_direction_map = {
    # token: [from]
    '|': [Direction.Down, Direction.Up],
    '-': [Direction.Left, Direction.Right],
    'L': [Direction.Down, Direction.Left],
    'J': [Direction.Down, Direction.Right],
    '7': [Direction.Right, Direction.Up],
    'F': [Direction.Left, Direction.Up],
    'S': [Direction.Up, Direction.Down, Direction.Left, Direction.Right],
    '.': []
}


def parse_input(lines):
    return [[x for x in l.strip()] for l in lines]


def neigh_coordinate(x, y, dir):
    neigh_x = x + 1 if dir == Direction.Right else x - 1\
        if dir == Direction.Left else x
    neigh_y = y + 1 if dir == Direction.Down else y - 1\
        if dir == Direction.Up else y
    return neigh_x, neigh_y


def is_neighbour(grid, x, y, neigh_x, neigh_y, dir):
    if neigh_x < 0 or neigh_x >= len(grid[0]):
        return False

    if neigh_y < 0 or neigh_y >= len(grid):
        return False

    token = grid[y][x]
    neigh_token = grid[neigh_y][neigh_x]

    can_move_to = [complement(x) for x in g_token_direction_map[token]]
    can_move_from = g_token_direction_map[neigh_token]
    return dir in can_move_to and dir in can_move_from


def neighbours(grid, x, y):
    neighs = []
    dirs = [Direction.Up, Direction.Down, Direction.Left, Direction.Right]
    for d in dirs:
        neigh_x, neigh_y = neigh_coordinate(x, y, d)
        if is_neighbour(grid, x, y, neigh_x, neigh_y, d):
            neighs.append((neigh_x, neigh_y))
    return neighs


def find_main_loop(grid):
    S = next((x, y) for y in range(len(grid))
             for x in range(len(grid[0])) if grid[y][x] == 'S')

    seen = set()
    longest_loop = []
    stack = [(S, [])]
    while stack:
        (x, y), steps = stack.pop()
        seen.add((x, y))
        neighs = neighbours(grid, x, y)
        for n_x, n_y in neighs:
            path = steps + [(n_x, n_y)]
            if (n_x, n_y) == S:
                longest_loop = path if len(path) > len(
                    longest_loop) else longest_loop
                continue

            if (n_x, n_y) not in seen:
                stack.append(((n_x, n_y), path))

    return longest_loop


def longest_step_in_loop(grid):
    return len(find_main_loop(grid)) // 2


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    print(longest_step_in_loop(grid))
