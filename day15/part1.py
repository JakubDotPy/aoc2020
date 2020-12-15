import argparse
import collections
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
"""


def compute(s: str) -> int:
    memory = collections.defaultdict(list)
    numbers = [int(n) for n in s.strip().split(',')]

    for turn, number in enumerate(numbers, start=1):
        memory[number].append(turn)

    say = numbers[-1]
    for turn in range(turn + 1, 2021):

        if len(memory[say]) == 1:
            say = 0
        else:
            say_seen = memory[say]
            say = say_seen[-1] - say_seen[-2]

        memory[say].append(turn)

    return say


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('0, 3, 6', 436),
            ('1, 3, 2', 1),
            ('2, 1, 3', 10),
            ('1, 2, 3', 27),
            ('2, 3, 1', 78),
            ('2, 3, 1', 78),
            ('3, 2, 1', 438),
            ('3, 1, 2', 1836),
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
