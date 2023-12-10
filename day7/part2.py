import sys
from part1 import score_histogram, value, parse_input, make_histogram

g_P2_order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']


def kind(hand):
    hist = make_histogram(hand)
    recepient = None
    try:
        donor = next((occu, card, idx)
                     for idx, (card, occu) in enumerate(hist) if card == 'J')
        recepient = max((occu, card, idx)
                        for idx, (card, occu) in enumerate(hist) if card != 'J')
    except:
        pass

    if recepient:
        old_occu, card, ridx = recepient
        j_occu, _, jidx = donor
        hist[ridx] = (card, old_occu + j_occu)
        hist.pop(jidx)

    return score_histogram(hist)


if __name__ == "__main__":
    bets = parse_input(sys.stdin)
    bets = sorted(bets, key=lambda x: value(x, kind, g_P2_order))
    winning = [(idx + 1) * int(bet) for idx, (_, bet) in enumerate(bets)]
    print(sum(winning))
