import argparse
import os.path
from collections import Counter

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def compute(s: str) -> int:
    lengths = []
    for group in s.split('\n\n'):
        group_counter = Counter()
        people = group.split('\n')
        num_people = len(people)

        for person_answer in people:
            group_counter.update(set(person_answer))

        all_answered = sum(True if cnt == num_people else False for cnt in group_counter.values())
        lengths.append(all_answered)

    return sum(lengths)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 6),
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
