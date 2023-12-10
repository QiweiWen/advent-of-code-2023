import sys


def parse_input(lines):
    return [tuple(l.split()) for l in lines]


def score_histogram(histogram):
    if len(histogram) == 1:
        return 7

    if len(histogram) == 2:
        occu = max(y for _, y in histogram)
        return 6 if occu == 4 else 5

    if len(histogram) == 3:
        occu = max(y for _, y in histogram)
        return 4 if occu == 3 else 3

    if len(histogram) == 4:
        return 2

    return 1


def make_histogram(hand):
    hand = sorted(hand)
    histogram = []
    occurrences = 1
    last = None
    for card in hand:
        if last and card != last:
            histogram.append((last, occurrences))
            occurrences = 1
            last = card
            continue

        if not last:
            last = card
        else:
            occurrences += 1

    if occurrences:
        histogram.append((last, occurrences))
    return histogram


def kind(hand):
    hist = make_histogram(hand)
    return score_histogram(hist)


g_P1_order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


def value(hand_and_bet, kind_func, order):
    hand = hand_and_bet[0]
    order = {y: len(order) - x for x, y in enumerate(order)}
    hand_rank = tuple(order[x] for x in hand)
    return (kind_func(hand), hand_rank)


if __name__ == "__main__":
    bets = parse_input(sys.stdin)
    bets = sorted(bets, key=lambda x: value(x, kind, g_P1_order))
    winning = [(idx + 1) * int(bet) for idx, (_, bet) in enumerate(bets)]
    print(sum(winning))
