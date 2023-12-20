import sys
from collections import defaultdict


def parse_input(inf):
    splitted = (l.split() for l in inf)
    result = [(parts, [int(x) for x in seq.split(",")])
              for (parts, seq) in splitted]
    return result


def num_solutions(parts, seq):
    cache = defaultdict(int)
    cache[('#', len(parts), len(seq) - 1, 0)] = 1
    cache[('.', len(parts), len(seq) - 1, 0)] = 1

    for i in reversed(range(len(parts))):
        for j in reversed(range(len(seq))):
            for k in range(0, seq[j] + 1):
                for last in ("#", "."):
                    as_dot = 0
                    as_hash = 0

                    if last == '#':
                        as_dot = 0 if k > 0 else \
                            cache[(".", i + 1, j, 0)] if j == len(seq) - 1 else\
                            cache[(".", i + 1, j + 1,
                                   0 if j == len(seq) - 1 else seq[j + 1])]
                    else:
                        as_dot = cache[(".", i + 1, j, k)]

                    as_hash = 0 if k == 0 else cache[("#", i + 1, j, k - 1)]

                    cache[(last, i, j, k)] =\
                        as_dot if parts[i] == '.' else as_hash if parts[i] == '#' else as_dot + as_hash

    return cache[(".", 0, 0, seq[0])]


if __name__ == "__main__":
    input = parse_input(sys.stdin)
    print(sum((num_solutions(parts, seq) for (parts, seq) in input)))
