import argparse
import os.path
from collections import Counter
from itertools import tee

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

INPUT_S1 = """\
16
10
15
5
1
11
7
19
6
12
4
"""
INPUT_S2 = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


def compute(s: str) -> int:
    nums = sorted(int(n) for n in s.splitlines())

    outlet_joltage = 0
    device_joltage = max(nums) + 3

    nums.insert(0, outlet_joltage)
    nums.append(device_joltage)

    p, n = tee(nums, 2)
    next(n, None)
    diffs = list(map(lambda tup: tup[1] - tup[0], zip(p, n)))
    distribution = Counter(diffs)

    return distribution[1] * distribution[3]


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S1, 35),
            (INPUT_S2, 220),
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
