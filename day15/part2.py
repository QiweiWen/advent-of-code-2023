import sys
from part1 import encode


def parse_input(inf):
    lenses = inf.read().strip().split(",")
    lenses = [lense.split("=") for lense in lenses]
    return lenses


def process_lenses(lenses):
    slots = [list() for i in range(0, 256)]

    for lense in lenses:
        if len(lense) == 2:
            label = lense[0]
            focus = int(lense[1])
        else:
            label = lense[0]
            label = label[0:len(label) - 1]
            focus = None

        slot = encode(label)
        try:
            idx = next(idx for idx, (l, focus)
                       in enumerate(slots[slot]) if label == l)
            if focus is None:
                slots[slot].pop(idx)
            else:
                slots[slot][idx] = (slots[slot][idx][0], focus)
        except StopIteration:
            idx = None
            if focus is not None:
                slots[slot].append((label, focus))
        
    score = 0 
    for i in range(256):
        box_score = i + 1
        for j in range(len(slots[i])):
            slot_score = j + 1
            focus_score = slots[i][j][1]
            score += (box_score * slot_score * focus_score)
    
    return score


if __name__ == "__main__":
    lenses = parse_input(sys.stdin)
    print(process_lenses(lenses))
