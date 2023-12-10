import sys
import re


def parse_input(lines):
    direction = {}
    instruction = lines[0].strip()
    for l in lines[1:]:
        l = l.strip()
        if not l:
            continue

        regex = "(\S*)\s*=\s*\((\S*),\s*(\S*)\)"
        if match := re.match(regex, l):
            direction[match.group(1)] = (match.group(2), match.group(3))
    return instruction, direction


def next_node(curr, instruction, direction):
    dir_l, dir_r = direction[curr]
    return dir_r if instruction == 'R' else dir_l


def count_steps(instruction, direction):
    curr = "AAA"
    step = 0
    iidx = 0
    while curr != "ZZZ":
        curr = next_node(curr, instruction[iidx], direction)
        step += 1
        iidx = (iidx + 1) % len(instruction)
    return step


if __name__ == "__main__":
    i, d = parse_input([l for l in sys.stdin])
    print(count_steps(i, d))
