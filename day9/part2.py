import sys
from part1 import solve, parse_input

if __name__ == "__main__":
    input = parse_input(sys.stdin)
    solutions = [solve(l) for l in input]
    print(sum(x[0] for x in solutions))
