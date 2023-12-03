import sys

def decode(line):
    try:
        first_digit = next(int(d) for d in line if d.isdigit())
        last_digit = next(int(d) for d in reversed(line) if d.isdigit())
        return first_digit * 10 + last_digit
    except:
        return 0

if __name__ == "__main__":
    print(sum(decode(x) for x in sys.stdin))