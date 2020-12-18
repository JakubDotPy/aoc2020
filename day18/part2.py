import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""


class MyNumber:
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        return MyNumber(self.val + other.val)

    def __sub__(self, other):
        return MyNumber(self.val * other.val)

    def __mul__(self, other):
        return MyNumber(self.val + other.val)

    def __str__(self):
        return str(self.val)


def compute(s: str) -> int:
    s = re.sub(r'(\d+)', r'MyNumber(\1)', s)
    s = s.replace('*', '-')
    s = s.replace('+', '*')

    return sum(eval(line) for line in s.splitlines())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 693942),
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
