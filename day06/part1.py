import argparse
import os.path

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

b
"""


def compute(s: str) -> int:
    lengths = []
    for group in s.split('\n\n'):
        group_set = set()
        for person_answ in group.split('\n'):
            group_set.update(set(person_answ))
        lengths.append(len(group_set))
    return sum(lengths)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 11),
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
