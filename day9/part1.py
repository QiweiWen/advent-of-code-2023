import sys
import functools


def parse_input(lines):
    return [[int(x) for x in l.split()] for l in lines]


def solve(nums):
    last_nums = [nums[-1]]
    first_nums = [nums[0]]
    while len(set(nums)) != 1:
        nums = [(nums[i + 1] - nums[i]) for i in range(len(nums) - 1)]
        last_nums.append(nums[-1])
        first_nums.append(nums[0])

    first_extrapolation = functools.reduce(
        lambda x, y: y - x, reversed(first_nums))
    return first_extrapolation, sum(last_nums)


if __name__ == "__main__":
    input = parse_input(sys.stdin)
    solutions = [solve(l) for l in input]
    print(sum(solutions))
