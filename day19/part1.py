import sys
import re


def parse_attribute(attribute):
    k, v = attribute.split("=")
    return int(v)


def parse_rule(rule):
    predicate, jump = rule.split(":")
    attribute = predicate[0]
    op = predicate[1]
    value = int(predicate[2:])

    def do_jump(attributes):
        x, m, a, s = attributes
        command = f"{attribute} {op} {value}"
        result = eval(command)
        return jump if result else None

    return do_jump


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


def run_rules(rules, part):
    outcome = "in"

    while outcome != 'A' and outcome != 'R':
        curr_ruleset = rules[outcome]
        ruleset, fallthrough = curr_ruleset
        for rule in ruleset:
            outcome = rule(part)
            if outcome:
                break

        if not outcome:
            outcome = fallthrough

    return outcome == 'A'


if __name__ == "__main__":
    rules, parts = parse_input(sys.stdin)
    accepted = [p for p in parts if run_rules(rules, p)]
    print(accepted)
    print(sum([sum(x) for x in accepted]))
