import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

INVALID_NUMBER = 258585477


# INVALID_NUMBER = 127


def compute(s: str) -> int:
    nums = [int(n) for n in s.splitlines()]

    for i, num in enumerate(nums):
        sequence = set()
        partial_sum = 0
        shift = 0
        while partial_sum < INVALID_NUMBER:
            partial_sum += nums[i + shift]
            sequence.add(nums[i + shift])
            shift += 1
        if partial_sum == INVALID_NUMBER:
            return min(sequence) + max(sequence)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 62),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
