from part1 import *
import sys

sys.path.append(os.path.join(os.getcwd(), os.pardir))
day16p1 = importlib.import_module("day16.part1")


def p2_search(grid):
    # loss, straight distance covered, curr direction, coordinates
    heap = [(0, (0, None, 0, 0))]
    seen = set()
    cost = dict()
    # heap_index = {(0, 0): 0}
    prev = dict()
    dests = set([
        (4, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (5, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (6, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (7, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (8, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (9, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (10, RIGHT, len(grid) - 1, len(grid[0]) - 1),
        (4, DOWN, len(grid) - 1, len(grid[0]) - 1),
        (5, DOWN, len(grid) - 1, len(grid[0]) - 1),
        (6, DOWN, len(grid) - 1, len(grid[0]) - 1),
        (7, DOWN, len(grid) - 1, len(grid[0]) - 1),
        (8, DOWN, len(grid) - 1, len(grid[0]) - 1),
        (9, DOWN, len(grid) - 1, len(grid[0]) - 1),
        (10, DOWN, len(grid) - 1, len(grid[0]) - 1)])

    to_see = dests.copy()

    while heap:
        uloss, (ustraight, udir, ui, uj) = heapq.heappop(heap)
        unode = (ustraight, udir, ui, uj)
        seen.add(unode)

        if unode in to_see:
            to_see.remove(unode)
            if not to_see:
                break

        vdirs = [LEFT, RIGHT, UP, DOWN]
        neighs = []
        for vdir in vdirs:
            if opposite(vdir, udir):
                continue

            if vdir == udir and ustraight == 10:
                continue

            if udir is not None and vdir != udir and ustraight < 4:
                continue

            vstraight = 1 if vdir != udir else ustraight + 1
            vi, vj = day16p1.move(ui, uj, vdir)
            if day16p1.inside(grid, vi, vj):
                neigh = (uloss + int(grid[vi][vj]),
                         (vstraight, vdir, vi, vj))
                neighs.append(neigh)

        for neigh in neighs:
            vloss, vnode = neigh
            vstraight, vdir, vi, vj = vnode
            vcost = (vloss << 16) + vstraight
            if vnode not in seen:
                old_vcost = cost.get(vnode)
                if old_vcost is not None and vcost >= old_vcost:
                    continue

                if old_vcost is not None:
                    for i_heap, (curr_loss, curr_node) in enumerate(heap):
                        if curr_node == vnode:
                            heap.pop(i_heap)
                            heapq.heapify(heap)
                            break

                cost[vnode] = vcost
                prev[vnode] = (ustraight, udir, ui, uj)
                heapq.heappush(heap, neigh)

    paths = [reconstruct_path(prev, x) for x in dests]
    return paths


if __name__ == "__main__":
    grid = day16p1.parse_input(sys.stdin)

    paths = p2_search(grid)
    for path in paths:
        print("path:")
        day16p1.draw_grid(grid, path)

    print(min(temp_loss(grid, x) for x in paths))
