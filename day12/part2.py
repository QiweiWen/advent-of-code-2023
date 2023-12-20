from part1 import *
import sys

if __name__ == "__main__":
    input = parse_input(sys.stdin)
    #input = [["?###????????", [3,2,1]]]
    #input = [("?#?#?#?#?#?#?#?",[1,3,1,6])]
    input = [("?".join([parts] * 5), seq * 5) for (parts, seq) in input]
    print(sum((num_solutions(parts, seq) for (parts, seq) in input)))
