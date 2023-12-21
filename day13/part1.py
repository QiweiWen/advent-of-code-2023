import sys
from collections import defaultdict


def parse_input(inf):
    patterns = []
    pattern = []
    for l in inf:
        l = l.strip()
        if pattern and not l:
            patterns.append(pattern)
            pattern = []
            continue
        if l:
            pattern.append(l)

    if pattern:
        patterns.append(pattern)

    return patterns


def rotated(pattern):
    return ["".join(x[i] for x in pattern) for i in range(len(pattern[0]))]


def compress(str):
    str = str.replace(".", "0")
    str = str.replace("#", "1")
    return int(str, 2)


def solve(pattern):
    nrows = len(pattern)
    cache = dict()

    for i in range(1, nrows):
        nbefore = i
        nafter = nrows - i
        symmetrical = True
        for j in range(0, min(nbefore, nafter)):
            one = i - j - 1
            other = i + j

            one_compressed = cache.get(one)
            if one_compressed is None:
                one_compressed = compress(pattern[one])
                cache[one] = one_compressed

            other_compressed = cache.get(other)
            if other_compressed is None:
                other_compressed = compress(pattern[other])
                cache[other] = other_compressed

            if one_compressed != other_compressed:
                symmetrical = False
                break

        if symmetrical:
            return i

    return 0


if __name__ == "__main__":
    patterns = parse_input(sys.stdin)
    score = sum(100 * solve(pattern) + solve(rotated(pattern))
                for pattern in patterns)
    print(score)
