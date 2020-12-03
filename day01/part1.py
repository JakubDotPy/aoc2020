import argparse

import pytest

from support.support import timing


def compute(s: str) -> int:
    nums = set(map(int, s.splitlines()))
    for num in nums:
        if 2020 - num in nums:
            return num * (2020 - num)

INPUT_S = """\
1721
979
366
299
675
1456
"""

@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 514579),
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
