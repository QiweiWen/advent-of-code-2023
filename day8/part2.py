import sys
from part1 import parse_input, next_node
import math


def ended(nodes):
    try:
        next(x for x in nodes if not x.endswith("Z"))
        return False
    except:
        return True


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm_list(nums):
    if len(nums) < 2:
        return nums[0]

    curr = lcm(nums[0], nums[1])
    for num in nums[2:]:
        curr = lcm(curr, num)

    return curr


def modes(start, instructions, direction):
    seen = set()
    iidx = 0
    steps = 0
    curr = start
    modes = []
    while True:
        curr_key = (curr, iidx)
        if curr_key in seen:
            break

        seen.add(curr_key)
        curr = next_node(curr, instructions[iidx], direction)
        iidx = (iidx + 1) % len(instructions)
        steps += 1

        if curr.endswith("Z"):
            modes.append(steps)

    return modes


def count_steps(instructions, direction):
    curr_nodes = set([x for x in sum(([x, y, z]
                                      for x, (y, z) in direction.items()), []) if x.endswith("A")])
    node_modes = [modes(x, instructions, direction) for x in curr_nodes]
    sequences = []
    stack = [(0, [x]) for x in node_modes[0]]

    while stack:
        node_idx, seq = stack.pop()
        if node_idx == len(node_modes) - 1:
            sequences.append(seq)
            continue

        children = node_modes[node_idx + 1]
        for mode in children:
            new_seq = seq + [mode]
            stack.append((node_idx + 1, new_seq))

    return min(lcm_list(x) for x in sequences)


if __name__ == "__main__":
    instructions, direction = parse_input([x for x in sys.stdin])
    print(count_steps(instructions, direction))
