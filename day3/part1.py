import sys


def find_all_parts(lines):
    parts = set()
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            char = line[j]
            if not char.isdigit() and char != ".":
                parts.add((i, j, char))
    return parts


def adjacent(row, cbegin, cend, parts):
    xbegin = cbegin - 1
    ybegin = row - 1
    xend = cend + 1
    yend = row + 1
    for x in range(xbegin, xend + 1):
        for y in range(ybegin, yend + 1):
            if (y, x) in parts:
                return True
    return False


def find_all_nums(lines):
    nums = []
    for row in range(len(lines)):
        line = lines[row]
        ybegin = None
        yend = None
        for column in range(len(line)):
            char = line[column]
            if char.isdigit():
                if ybegin is None:
                    ybegin = column
                    yend = column
                else:
                    yend += 1
            else:
                if ybegin is not None:
                    nums.append((row, ybegin, yend))
                    ybegin = None
        if ybegin is not None:
            nums.append((row, ybegin, yend))
    return nums


def to_num(lines, row, cbegin, cend):
    substr = lines[row][cbegin:cend + 1]
    return int(substr)


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]
    parts = {(x, y) for (x, y, _) in find_all_parts(lines)}
    nums = [(r, b, e)
            for (r, b, e) in find_all_nums(lines) if adjacent(r, b, e, parts)]
    print(sum(to_num(lines, r, b, e) for r, b, e in nums))
