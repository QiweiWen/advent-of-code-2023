import sys


def parse_input(inf):
    field = [l.strip() for l in inf]
    expanded_rows = [i for i, r in enumerate(field) if set(r) == set(".")]
    rotated = ["".join(x[i] for x in field) for i in range(len(field[0]))]
    expanded_cols = [i for i, c in enumerate(rotated) if set(c) == set(".")]
    expanded_field = []
    for r in range(len(field)):
        row = ""
        for c in range(len(field[r])):
            if c in expanded_cols:
                row += field[r][c]
            row += field[r][c]

        if r in expanded_rows:
            expanded_field.append(row)
        expanded_field.append(row)

    galaxies = [(y, x) for y in range(len(field))
                for x in range(len(field[0])) if field[y][x] == '#']
    expanded_galaxies = [(y, x) for y in range(len(expanded_field))
                         for x in range(len(expanded_field[0])) if expanded_field[y][x] == '#']

    return {
        "field": field,
        "expanded_rows": expanded_rows,
        "expanded_cols": expanded_cols,
        "expanded_field": expanded_field,
        "galaxies": galaxies,
        "expanded_galaxies": expanded_galaxies
    }


def galaxy_pairs(galaxies):
    return [(a, b) for a in galaxies for b in galaxies if a < b]


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


if __name__ == "__main__":
    input = parse_input(sys.stdin)
    pairs = galaxy_pairs(input["expanded_galaxies"])
    dists = [distance(x1, y1, x2, y2) for ((x1, y1), (x2, y2)) in pairs]
    print(sum(dists))
