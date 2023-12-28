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
    to_see = set([(RIGHT, len(grid) - 1, len(grid[0]) - 1),
                  (DOWN, len(grid) - 1, len(grid[0]) - 1)])

    while heap:
        (uloss, ustraight), (udir, ui, uj) = heapq.heappop(heap)
        # heap_index.pop((ui, uj))
        unode = (udir, ui, uj)
        seen.add(unode)

        print(f"POP {unode} == ({uloss}, {ustraight})", file=sys.stderr)

        if unode in to_see:
            to_see.remove(unode)
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
                neigh = ((uloss + int(grid[vi][vj]),
                         vstraight), (vdir, vi, vj))
                neighs.append(neigh)

        for neigh in neighs:
            (vloss, vstraight), vnode = neigh
            DEBUG = vnode == (1, 6, 11)
            vcost = (vloss << 16) + vstraight
            if vnode not in seen:
                old_vcost = cost.get(vnode)
                if old_vcost is not None and vcost >= old_vcost:
                    continue

                if old_vcost is not None:
                    for i_heap, ((curr_loss, curr_straight), curr_node) in enumerate(heap):
                        if curr_node == vnode:
                            heap.pop(i_heap)
                            heapq.heapify(heap)
                            break

                cost[vnode] = vcost
                prev[vnode] = (udir, ui, uj)
                heapq.heappush(heap, neigh)
                print(f"PUSH {neigh}", file=sys.stderr)

    curr_dir = RIGHT
    rpath = [(ui, uj)]
    while rpath[0] != (0, 0):
        curr_i, curr_j = rpath[0]
        curr_dir, next_i, next_j = prev[(curr_dir, curr_i, curr_j)]
        rpath.insert(0, (next_i, next_j))

    curr_dir = DOWN
    dpath = [(ui, uj)]
    while dpath[0] != (0, 0):
        curr_i, curr_j = dpath[0]
        curr_dir, next_i, next_j = prev[(curr_dir, curr_i, curr_j)]
        dpath.insert(0, (next_i, next_j))

    return rpath, dpath


def temp_loss(grid, path):
    return sum(int(grid[i][j]) for (i, j) in path if i != 0 or j != 0)


if __name__ == "__main__":
    grid = day16p1.parse_input(sys.stdin)
    rpath, dpath = search(grid)
    print("rpath:")
    day16p1.draw_grid(grid, rpath)
    print("dpath:")
    day16p1.draw_grid(grid, dpath)

    print(min(temp_loss(grid, rpath), temp_loss(grid, dpath)))
