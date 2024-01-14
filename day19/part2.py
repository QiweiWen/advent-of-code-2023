import sys
import re
from enum import Enum


def parse_attribute(attribute):
    k, v = attribute.split("=")
    return int(v)


def parse_rule(rule):
    predicate, jump = rule.split(":")
    return (predicate, jump)


def parse_input(inf):
    rules = {}
    parts = []
    for line in inf:
        # px{a<2006:qkq,m>2090:A,rfg}
        rule_regex = "(.+){(.*),(.*)}"
        # {x=787,m=2655,a=1222,s=2876}
        part_regex = "{(.*)}"

        if match := re.match(rule_regex, line):
            rule_name = match.group(1)
            ruleset = [parse_rule(x) for x in match.group(2).split(",")]
            fallthrough = match.group(3)
            rules[rule_name] = (ruleset, fallthrough)
        elif match := re.match(part_regex, line):
            attributes = [parse_attribute(x)
                          for x in match.group(1).split(",")]
            parts.append(attributes)

    return rules, parts


def reconstruct_path(parent_dict, node):
    path = [node]
    while node[1] != 'in':
        parent_node = parent_dict[node]
        path.insert(0, parent_node)
        node = parent_node
    return path


def gen_accepted_paths(rules):
    stack = [(None, "in")]
    parent = {}

    while stack:
        curr_node = stack[-1]
        parent_idx, ruleset_name = curr_node
        stack.pop()

        if ruleset_name == 'A':
            yield reconstruct_path(parent, curr_node)
            continue

        if ruleset_name == 'R':
            continue

        def push_neighbour(idx, name):
            neigh_node = (idx, name)
            parent[neigh_node] = curr_node
            stack.append(neigh_node)

        ruleset = rules[ruleset_name]
        predicates, fallthrough = ruleset

        push_neighbour(None, fallthrough)
        for i in range(len(predicates)):
            predicate, jump = predicates[i]
            push_neighbour(i, jump)


# "a<2006"
def parse_predicate(pred_string):
    attribute = pred_string[0]
    operation = pred_string[1]
    value = int(pred_string[2:])
    return attribute, operation, value


def constrain_one(rule_string, opposite, x, m, a, s):
    attr, op, val = parse_predicate(rule_string)
    lower, upper = locals()[attr]
    if opposite:
        if op == '<':
            op = '>'
            val -= 1
        else:
            op = '<'
            val += 1

    if op == '<':
        upper = min(val - 1, upper)
    if op == '>':
        lower = max(val + 1, lower)

    # interpreter bug
    if attr == 'x':
        x = (lower, upper)
    if attr == 'm':
        m = (lower, upper)
    if attr == 'a':
        a = (lower, upper)
    if attr == 's':
        s = (lower, upper)

    return (x, m, a, s)


def invalid(x, m, a, s):
    return any((r for r in [x, m, a, s] if r[0] > r[1]))


def constrain(rules, path, x, m, a, s):
    for i in range(len(path) - 1):
        _, rule_name = path[i]
        rule_idx, _ = path[i + 1]

        predicates, fallthrough = rules[rule_name]
        for idx, (predicate, jump) in enumerate(predicates):
            if idx == rule_idx:
                x, m, a, s = constrain_one(predicate, False, x, m, a, s)
                break
            x, m, a, s = constrain_one(predicate, True, x, m, a, s)

    return x, m, a, s


def range_len(range):
    min, max = range
    return max - min + 1


if __name__ == "__main__":
    rules, parts = parse_input(sys.stdin)
    paths = list(gen_accepted_paths(rules))

    combs = 0
    xi = (1, 4000)
    mi = (1, 4000)
    ai = (1, 4000)
    si = (1, 4000)

    for path in paths:
        constrained = constrain(rules, path, xi, mi, ai, si)
        if not constrained:
            continue
        x, m, a, s = constrained
        combs += range_len(x) * range_len(m) * range_len(a) * range_len(s)
    print(combs)
