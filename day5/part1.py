import sys
import re
from collections import defaultdict


def parse_input(lines):
    seeds = lines[0].split(":")[1].split(" ")
    seeds = [int(s.strip()) for s in seeds if s]
    lines = (l.strip() for l in lines[1:])
    maps = []
    curr_map = None
    special_ranges = []
    regex = "(.*)-to-(.*)\s+map"
    for l in lines:
        if not l:
            if curr_map:
                curr_map["special_ranges"] = special_ranges
                maps.append(curr_map)
                curr_map = None
            continue

        if curr_map is None:
            match = re.match(regex, l)
            if not match:
                return None

            from_category = match.group(1).strip()
            to_category = match.group(2).strip()
            curr_map = {"from": from_category, "to": to_category}
            special_ranges = []
            continue

        range = [int(x) for x in l.split(" ") if x]
        special_ranges.append(range)

    if curr_map:
        curr_map["special_ranges"] = special_ranges
        maps.append(curr_map)

    return maps, seeds


def map_value(ranges, from_value):
    for r in ranges:
        dst_start, src_start, length = r
        if from_value >= src_start and from_value < src_start + length:
            return dst_start + from_value - src_start
    return from_value


def map_category(from_category, to_category, from_values, maps):
    maps_dict = {x["from"]: x for x in maps}
    curr = from_category
    values = from_values
    while curr != to_category:
        next = maps_dict[curr]
        values = [map_value(next["special_ranges"], v) for v in values]
        curr = next["to"]
    return values


if __name__ == "__main__":
    maps, seeds = parse_input([x for x in sys.stdin])
    print(min(map_category("seed", "location", seeds, maps)))
