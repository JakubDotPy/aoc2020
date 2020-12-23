import argparse
import os.path
from collections import deque

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
389125467"""


def compute(s: str) -> int:
    cups = deque(map(int, s))

    for move in range(1, 100 + 1):
        print(f'-- move {move} --')
        print(f'cups: {cups}')

        current = cups[0]
        next_current = cups[4]

        # pick three after current
        cups.rotate(-1)
        pick_up = [cups.popleft() for _ in range(3)]

        print(f'pick up: {pick_up}')

        # find index
        minimal, maximal = min(cups), max(cups)
        placement = current - 1
        while placement not in cups:
            if placement < minimal:
                placement = maximal
                break
            placement -= 1
        print(f'destination: {placement}')
        place_where = cups.index(placement)

        # insert
        for element in pick_up[::-1]:
            cups.insert(place_where + 1, element)

        while cups[0] != next_current:
            cups.rotate()

    # rotate to final position
    while cups[0] != 1:
        cups.rotate()

    return ''.join(map(str, list(cups)[1:]))


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, '67384529'),
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
