import sys


def roll_north(row, grid):
    for i in range(len(grid[row])):
        if grid[row][i] == 'O':
            target = row
            for j in reversed(range(0, row)):
                if grid[j][i] != '.':
                    break
                target = j

            if row != target:
                grid[target][i] = 'O'
                grid[row][i] = '.'


def parse_input(inf):
    return [[y for y in x.strip()] for x in inf if x]


def print_grid(grid):
    for row in grid:
        print("".join(row))


def cost(grid):
    sum = 0
    for row in range(len(grid)):
        load = len(grid) - row
        for col in range(len(grid[row])):
            if grid[row][col] == 'O':
                sum += load
    return sum


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    # print("before:")
    # print_grid(grid)
    for row in range(1, len(grid)):
        roll_north(row, grid)
    print(cost(grid))

    # print("after:")
    # print_grid(grid)
