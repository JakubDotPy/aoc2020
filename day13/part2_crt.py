import argparse
import os.path

import pytest
from sympy.ntheory.modular import crt

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
939
7,13,x,x,59,x,31,19
"""


def compute(s: str) -> int:
    lines = s.splitlines()
    busses = [
        (int(s), i)
        for i, s in enumerate(lines[1].split(','))
        if s != 'x'
        ]
    busses_num = [pt[0] for pt in busses]
    busses_offs = [-1 * pt[1] for pt in busses]

    return crt(busses_num, busses_offs)[0]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('7,13,x,x,59,x,31,19', 1068781),
            ('17,x,13,19', 3417),
            ('67,7,59,61', 754018),
            ('67,x,7,59,61', 779210),
            ('67,7,x,59,61', 1261476),
            ('1789,37,47,1889', 1202161486),
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
