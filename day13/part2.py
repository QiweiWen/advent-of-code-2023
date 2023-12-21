import part1
import sys
import math


def is_pow2(n):
    return (n & (n-1) == 0) and n != 0


def solve_smudge(pattern):
    nrows = len(pattern)
    cache = dict()

    for i in range(1, nrows):
        nbefore = i
        nafter = nrows - i
        symmetrical = True
        smudge_found = False
        for j in range(0, min(nbefore, nafter)):
            one = i - j - 1
            other = i + j

            one_compressed = cache.get(one)
            if one_compressed is None:
                one_compressed = part1.compress(pattern[one])
                cache[one] = one_compressed

            other_compressed = cache.get(other)
            if other_compressed is None:
                other_compressed = part1.compress(pattern[other])
                cache[other] = other_compressed

            xor = one_compressed ^ other_compressed
            if one_compressed != other_compressed and not is_pow2(xor):
                symmetrical = False
                break

            if smudge_found and one_compressed != other_compressed:
                symmetrical = False
                break

            if not smudge_found:
                if is_pow2(xor):
                    smudge_found = True

        if symmetrical and smudge_found:
            return i

    return 0


def solve(pattern):
    horizontal = solve_smudge(pattern)
    vertical = solve_smudge(part1.rotated(pattern))
    assert (not horizontal or not vertical)
    return vertical if vertical else 100 * horizontal


if __name__ == "__main__":
    patterns = part1.parse_input(sys.stdin)
    score = sum(solve(pattern) for pattern in patterns)
    print(score)
