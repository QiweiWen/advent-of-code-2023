import sys
import os
import importlib
import heapq

sys.path.append(os.path.join(os.getcwd(), os.pardir))
day16p1 = importlib.import_module("day16.part1")


UP = day16p1.UP
DOWN = day16p1.DOWN
LEFT = day16p1.LEFT
RIGHT = day16p1.RIGHT


def opposite(dir1, dir2):
    return dir1 == UP and dir2 == DOWN or dir1 == DOWN and dir2 == UP or\
        dir1 == LEFT and dir2 == RIGHT or dir1 == RIGHT and dir2 == LEFT


def search(grid):
    # loss, straight distance covered, curr direction, coordinates
    heap = [(0, 0, None, (0, 0))]
    seen = set()
    cost = dict()
    # heap_index = {(0, 0): 0}
    prev = dict()
    while heap:
        uloss, ustraight, udir, (ui, uj) = heapq.heappop(heap)
        # heap_index.pop((ui, uj))
        seen.add((ui, uj))

        if (ui < 5 and uj < 5):
            print(f"POP {(uloss, ustraight, udir, (ui, uj))}", file=sys.stderr)

        if ui == len(grid) - 1 and uj == len(grid[ui]) - 1:
            break

        vdirs = [LEFT, RIGHT, UP, DOWN]
        neighs = []
        for vdir in vdirs:
            if opposite(vdir, udir):
                continue

            if vdir == udir and ustraight == 3:
                continue

            vstraight = 1 if vdir != udir else ustraight + 1
            vi, vj = day16p1.move(ui, uj, vdir)
            if day16p1.inside(grid, vi, vj):
                neigh = (uloss + int(grid[vi][vj]), vstraight, vdir, (vi, vj))
                neighs.append(neigh)

        for vcost, vstraight, vdir, (vi, vj) in neighs:
            if (vi, vj) not in seen:
                old_vcost = cost.get((vi, vj))
                if old_vcost is not None and vcost >= old_vcost:
                    continue

                if old_vcost is not None:
                    for i_heap in enumerate(heap):
                        _, _, (curr_i, curr_j) = heap[i_heap]
                        if curr_i == vi and curr_j == vj:
                            heap.pop(i_heap)
                            heapq.heapify(i_heap)
                            break

                cost[(vi, vj)] = vcost
                prev[(vi, vj)] = (ui, uj)
                heapq.heappush(heap, (vcost, vstraight, vdir, (vi, vj)))

                if (vi < 5 and vj < 5):
                    print(
                        f"PUSH {(vcost, vstraight, vdir, (vi, vj))}", file=sys.stderr)

    path = [(ui, uj)]
    while path[0] != (0, 0):
        path.insert(0, prev[path[0]])

    return path


def temp_loss(grid, path):
    return sum(int(grid[i][j]) for (i, j) in path if i != 0 or j != 0)


if __name__ == "__main__":
    grid = day16p1.parse_input(sys.stdin)
    path = search(grid)
    day16p1.draw_grid(grid, path)
    print(temp_loss(grid, path))
