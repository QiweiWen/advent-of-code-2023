import sys
import re


def parse_input(lines):
    input = []
    for l in lines:
        regex = "^Card\s*([0-9]*):(.*)\|(.*)$"
        match = re.match(regex, l)
        if not match:
            return None

        id = match.group(1)
        haves = [x.strip() for x in match.group(2).split(" ")]
        wins = [x.strip() for x in match.group(3).split(" ")]
        input.append({
            "have": [int(x) for x in haves if x.isdigit()],
            "wins": {int(x) for x in wins if x.isdigit()},
        })

    return input


def num_matches(card):
    return len([x for x in card["have"] if x in card["wins"]])


def num_points(card):
    num_wins = num_matches(card)
    return 2 ** (num_wins - 1) if num_wins else 0


if __name__ == "__main__":
    cards = parse_input(l for l in sys.stdin)
    print(sum(num_points(x) for x in cards))
