import argparse

import pytest

from support.support import timing
from collections import Counter


def compute(s: str) -> int:
    rows = s.splitlines()
    count = 0
    for row in rows:
        splits = row.split()
        (min_n, max_n), letter, pwd = splits[0].split('-'), splits[1][0], splits[2]
        pwd_cnt = Counter(pwd)
        valid = int(min_n) <= pwd_cnt[letter] <= int(max_n)
        count += valid
    return count


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (f"1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc", 2),
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
