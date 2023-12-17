import sys


def parse_input(inf):
    field = [l.strip() for l in inf]
    expanded_rows = [i for i, r in enumerate(field) if set(r) == set(".")]
    rotated = ["".join(r[i] for r in field) for i in range(len(field[0]))]
    expanded_cols = [i for i, c in enumerate(rotated) if set(c) == set(".")]

    galaxies = [(r, c) for r in range(len(field))
                for c in range(len(field[0])) if field[r][c] == '#']

    return {
        "field": field,
        "expanded_rows": expanded_rows,
        "expanded_cols": expanded_cols,
        "galaxies": galaxies,
    }


def galaxy_pairs(galaxies):
    return [(a, b) for a in galaxies for b in galaxies if a < b]


def distance(r1, c1, r2, c2, expanded_rows, expanded_cols, factor=2):
    rmin = min(r1, r2)
    rmax = max(r1, r2)
    cmin = min(c1, c2)
    cmax = max(c1, c2)
    affected_rows = sum(1 for r in expanded_rows if r > rmin and r < rmax)
    affected_cols = sum(1 for c in expanded_cols if c > cmin and c < cmax)
    return abs(r2 - r1) + (factor - 1) * affected_rows + abs(c2 - c1) + (factor - 1) * affected_cols


if __name__ == "__main__":
    factor = int(sys.argv[1])
    input = parse_input(sys.stdin)
    pairs = galaxy_pairs(input["galaxies"])
    dists = [distance(r1, c1, r2, c2, input["expanded_rows"],
                      input["expanded_cols"], factor) for ((r1, c1), (r2, c2)) in pairs]
    print(sum(dists))
