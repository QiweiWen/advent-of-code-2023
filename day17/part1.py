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
    heap = [((0, 0), (None, 0, 0))]
    seen = set()
    cost = dict()
    # heap_index = {(0, 0): 0}
    prev = dict()
    to_see = set((LEFT, len(grid) - 1, len(grid[0]) - 1),
                 (DOWN, len(grid) - 1, len(grid[0]) - 1))

    while heap:
        (uloss, ustraight), (udir, ui, uj) = heapq.heappop(heap)
        # heap_index.pop((ui, uj))
        seen.add((udir, ui, uj))

        to_see.pop((udir, ui, uj))
        if not to_see:
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
                neigh = ((uloss + int(grid[vi][vj]), vstraight), (vdir, vi, vj))
                neighs.append(neigh)

        for neigh in neighs:
            (vloss, vstraight), (vdir, vi, vj) = neigh
            vcost = vloss << 16 + vstraight
            if (vdir, vi, vj) not in seen:
                old_vcost = cost.get((vdir, vi, vj))
                if old_vcost is not None and vcost >= old_vcost:
                    continue

                if old_vcost is not None:
                    for i_heap in enumerate(heap):
                        _, (curr_dir, curr_i, curr_j) = heap[i_heap]
                        if curr_dir == vdir and curr_i == vi and curr_j == vj:
                            heap.pop(i_heap)
                            heapq.heapify(i_heap)
                            break

                cost[(vdir, vi, vj)] = vcost
                prev[(vdir, vi, vj)] = (udir, ui, uj)
                heapq.heappush(heap, neigh) 

    rpath = [(RIGHT, ui, uj)]
    while rpath[0] != (None, 0, 0):
        rpath.insert(0, prev[path[0]])

    dpath = [(DOWN, ui, uj)]
    while dpath[0] != (None, 0, 0):
        dpath.insert(0, prev[path[0]])

    return dpath


def temp_loss(grid, path):
    return sum(int(grid[i][j]) for (i, j) in path if i != 0 or j != 0)


if __name__ == "__main__":
    grid = day16p1.parse_input(sys.stdin)
    rpath, dpath = search(grid)
    print("rpath:")
    day16p1.draw_grid(grid, rpath)
    print("dpath:")
    day16p1.draw_grid(grid, dpath)
