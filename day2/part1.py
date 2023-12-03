import sys
import re


def decode(line):
    regex = "^Game\s*([0-9]+):(.*)$"
    match = re.match(regex, line)
    if match:
        id = int(match.group(1))
        draws = [x.split(",") for x in match.group(2).split(";")]

        R = []
        G = []
        B = []
        regex = "\s*([0-9]+)\s*(red|green|blue)\s*"
        for d in draws:
            for colour in d:
                match = re.match(regex, colour)
                if not match:
                    return None

                if match.group(2) == "red":
                    R.append(int(match.group(1)))
                elif match.group(2) == "blue":
                    B.append(int(match.group(1)))
                elif match.group(2) == "green":
                    G.append(int(match.group(1)))

        return {"id": id, "red": R, "green": G, "blue": B}


def possible(decoded):
    if not decoded:
        return 0
    return decoded["id"] if max(decoded["blue"]) <= 14 and max(decoded["green"]) <= 13 and max(decoded["red"]) <= 12 else 0


if __name__ == "__main__":
    print(sum(possible(decode(x)) for x in sys.stdin))
