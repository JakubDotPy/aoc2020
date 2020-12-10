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


def compute(s: str, preamble_len=25) -> int:
    nums = [int(n) for n in s.splitlines()]

    for i, num in enumerate(nums):
        if i < preamble_len:
            continue  # skip preamble
        source, to_check = num, set(nums[i - preamble_len:i])
        checked = set()
        for test in to_check:
            checked.add(test)
            if source - test in to_check:
                break
            if checked == to_check:
                # we checked all, not found
                return source


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 127),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, preamble_len=5) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
