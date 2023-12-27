import sys

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


def parse_input(inf):
    return [x.strip() for x in inf]


def reflect(dir, mirror):
    if mirror == '/':
        if dir == LEFT:
            return [DOWN]
        if dir == DOWN:
            return [LEFT]
        if dir == RIGHT:
            return [UP]
        if dir == UP:
            return [RIGHT]
    if mirror == '\\':
        if dir == LEFT:
            return [UP]
        if dir == DOWN:
            return [RIGHT]
        if dir == RIGHT:
            return [DOWN]
        if dir == UP:
            return [LEFT]
    if mirror == '|':
        if dir == UP or dir == DOWN:
            return [dir]
        if dir == LEFT or dir == RIGHT:
            return [UP, DOWN]
    if mirror == '-':
        if dir == LEFT or dir == RIGHT:
            return [dir]
        if dir == UP or dir == DOWN:
            return [LEFT, RIGHT]
    return [dir]


def inside(grid, i, j):
    return i >= 0 and j >= 0 and i < len(grid) and j < len(grid[0])


def move(i, j, dir):
    if dir == UP:
        return (i - 1, j)
    if dir == DOWN:
        return (i + 1, j)
    if dir == LEFT:
        return (i, j - 1)
    if dir == RIGHT:
        return (i, j + 1)


def energise(grid, init=((0, -1), RIGHT)):
    queue = [init]
    seen = set()
    energised = set()
    while queue:
        (i, j), dir = queue[0]
        queue = queue[1:]

        if inside(grid, i, j):
            seen.add(((i, j), dir))
            energised.add((i, j))

        next_i, next_j = move(i, j, dir)
        if not inside(grid, next_i, next_j):
            continue

        next_dirs = reflect(dir, grid[next_i][next_j])
        for next_dir in next_dirs:
            if ((next_i, next_j), next_dir) not in seen:
                queue.append(((next_i, next_j), next_dir))

    return energised


def draw_grid(grid, energised):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in energised:
                print(grid[i][j], end="")
            else:
                print(f"\033[92m{grid[i][j]}\033[0m", end="")
        print("")


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    energised = energise(grid)
    draw_grid(grid, energised)
    print(len(energised))
