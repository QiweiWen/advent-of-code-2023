from part1 import parse_input, num_matches
import sys


def spawn(cards):
    stack = []
    num_insertions = 0
    curr = 0

    while curr < len(cards) or stack:
        if not stack:
            num_insertions += 1
            stack.append(curr)
            curr += 1
            continue

        top_idx = stack.pop()
        top_card = cards[top_idx]
        spawns = range(top_idx + 1, top_idx + 1 + num_matches(top_card))
        for spawn in spawns:
            stack.append(spawn)
            num_insertions += 1

    return num_insertions


cards = parse_input(l for l in sys.stdin)
print(spawn(cards))