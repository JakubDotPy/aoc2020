import argparse
import itertools
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
939
7,13,x,x,59,x,31,19
"""


def compute(s: str) -> int:
    busses = list(
        (int(bus_period), i)
        for i, bus_period in enumerate(s.split(','), start=1)
        if bus_period != 'x'
        )

    max_bus, max_bus_index = max(busses, key=lambda x: x[0])
    min_bus, min_bus_index = min(busses, key=lambda x: x[0])

    def check_condition(number):
        checks = set()
        nums = set()
        for bus, index in busses:
            index_offset = max_bus_index - index
            to_check = number - index_offset
            check = to_check % bus == 0
            nums.add(to_check)
            checks.add(check)
        return all(checks), nums

    counter = itertools.count(start=1)
    for i in counter:
        mul_number = max_bus * i
        condition, numbers = check_condition(mul_number)
        if condition:
            return min(numbers)


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
