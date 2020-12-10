import argparse
import os.path
from collections import defaultdict

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
    """based on solution from Lubos Kolouch"""
    nums = sorted(int(n) for n in s.splitlines())

    paths = defaultdict(int)
    paths[0] = 1

    for item in nums:
        paths[item] = paths[item - 1] + paths[item - 2] + paths[item - 3]

    return paths[nums[-1]]


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S1, 8),
            (INPUT_S2, 19208),
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
