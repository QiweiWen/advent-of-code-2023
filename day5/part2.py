from part1 import parse_input
import sys


def intersect(s1, l1, s2, l2):
    if s2 < s1 or s2 >= s1 + l1:
        return None

    head = (s1, s2 - s1)
    tail1 = None
    tail2 = None
    offset = s2 - s1
    if l2 < (l1 - offset):
        middle = (s2, l2)
        tail1 = (offset + s2, l1 - offset - l2)
    else:
        middle = (s2, l1 - offset)
        tail2 = (s1 + l1, l2 - (l1 - offset))

    result = [head, middle, tail1, tail2]
    result = [x if x and x[1] else None for x in result]
    return result

# map from_range into a series of dst ranges


def map_range(special_ranges, from_range):
    to_ranges = []
    unmapped = [from_range]
    while unmapped:
        unmapped_range = unmapped.pop()
        is_special = False
        for special in special_ranges:
            dst, src, length = special
            unmapped_src, unmapped_length = unmapped_range
            if inter := intersect(src, length, unmapped_src, unmapped_length):
                is_special = True
                left_head = None
                _, mapped, _, left_tail = inter
                mapped = (unmapped_src - src + dst, mapped[1])
            elif inter := intersect(unmapped_src, unmapped_length, src, length):
                is_special = True
                left_head, mapped, left_tail, _ = inter
                mapped = (dst, mapped[1])

            if is_special:
                if left_head:
                    unmapped.append(left_head)
                if left_tail:
                    unmapped.append(left_tail)
                to_ranges.append(mapped)
                break

        if not is_special:
            # does not fit into special range
            to_ranges.append(unmapped_range)

    return to_ranges


def map_category(from_category, to_category, from_ranges, maps):
    maps_dict = {x["from"]: x for x in maps}
    curr = from_category
    ranges = from_ranges
    while curr != to_category:
        next = maps_dict[curr]
        ranges = sum([map_range(next["special_ranges"], r)
                     for r in ranges], [])
        curr = next["to"]
    return ranges


maps, seed = parse_input([l for l in sys.stdin])
seed_ranges = [(seed[2 * x], seed[2 * x + 1]) for x in range(len(seed)//2)]
location_ranges = map_category("seed", "location", seed_ranges, maps)
print(min(location_ranges)[0])
