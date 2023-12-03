import sys
from part1 import find_all_parts, find_all_nums, to_num


def adjacent_nums(x, y, nums, lines):
    xbegin = x - 1
    xend = x + 1
    ybegin = y - 1
    yend = y + 1

    begin_dict = {(r, b): e for (r, b, e) in nums}
    end_dict = {(r, e): b for (r, b, e) in nums}

    neighs = []

    for xi in range(xbegin, xend + 1):
        for yi in range(ybegin, yend + 1):
            xe = begin_dict.get((yi, xi))
            if xe is not None:
                neighs.append(to_num(lines, yi, xi, xe))
                end_dict.pop((yi, xe))
                continue

            xb = end_dict.get((yi, xi))
            if xb is not None:
                neighs.append(to_num(lines, yi, xb, xi))
                begin_dict.pop((yi, xb))
                continue

    return neighs


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]
    gears = [(y, x) for (y, x, c) in find_all_parts(lines) if c == "*"]
    nums = find_all_nums(lines)
    neighs = [adjacent_nums(x, y, nums, lines) for (y, x) in gears]
    neighs = [n for n in neighs if len(n) == 2]
    print(sum((a * b) for a, b in neighs))
