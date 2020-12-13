import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
939
7,13,x,x,59,x,31,19
"""


def compute(s: str) -> int:
    departure, busses = s.splitlines()
    departure = int(departure)
    busses = set(int(bus_period) for bus_period in busses.split(',') if bus_period != 'x')

    wait_times = dict()
    for bus_period in busses:
        num_turns = (departure // bus_period) + 1
        next_departure = num_turns * bus_period
        wait_time = next_departure - departure
        wait_times[bus_period] = wait_time

    min_wait_bus = min(wait_times, key=wait_times.get)

    return min_wait_bus * wait_times[min_wait_bus]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 295),
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
