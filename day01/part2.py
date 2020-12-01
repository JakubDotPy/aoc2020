import argparse
from itertools import tee

import pytest

from support.support import timing


def compute(s: str) -> int:
    nums = sorted(set(map(int, s.splitlines())))
    a, b = tee(nums)
    next(b, None)
    for prev, nex in zip(a, b):
        search = 2020 - (prev + nex)
        if search in nums:
            return search * prev * nex


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""979
            366
            675
            299
            1456""", 241861950),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
