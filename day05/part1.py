import argparse
from math import ceil

import pytest

from support.support import timing


class Coords:

    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    @property
    def pivot(self):
        piv = ceil((self.upper - self.lower) / 2)
        return piv

    def __repr__(self):
        return f'Coords({self.lower}, {self.upper})'


def compute_seat(coords) -> (int, int):
    seat = (0, 0)
    row, col = Coords(0, 127), Coords(0, 7)
    row_dirs, col_dirs = coords[:7], coords[-3:]

    for half in row_dirs:
        if half == 'F':  # keep lower
            row.upper -= row.pivot
        if half == 'B':  # keep upper
            row.lower += row.pivot

    for half in col_dirs:
        if half == 'L':  # keep lower
            col.upper -= col.pivot
        if half == 'R':  # keep upper
            col.lower += col.pivot

    return row.upper, col.upper


def compute_id(seat) -> int:
    return seat[0] * 8 + seat[1]


def compute(s: str) -> int:
    ids = [compute_id(compute_seat(coords)) for coords in s.splitlines()]
    return max(ids)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('FBFBBFFRLR', 357),
            ('BFFFBBFRRR', 567),
            ('FFFBBBFRRR', 119),
            ('BBFFBBFRLL', 820),
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
