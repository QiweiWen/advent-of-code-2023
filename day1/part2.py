import sys


def decode(line):
    words = {"one": 1, "two": 2, "three": 3,
             "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

    word_occurrences = [(line.find(x), y) for x, y in words.items()] +\
        [(line.rfind(x), y) for x, y in words.items()]
    word_occurrences = [(x, y) for (x, y) in word_occurrences if x != -1]
    digit_occurrences = [(x, int(y))
                         for x, y in enumerate(line) if y.isdigit()]

    all_occurrences = word_occurrences + digit_occurrences
    if not all_occurrences:
        return 0

    _, first = min(all_occurrences)
    _, last = max(all_occurrences)
    return first * 10 + last


if __name__ == "__main__":
    print(sum(decode(line) for line in sys.stdin))
