import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
.#.
..#
###"""


GRID = dict()
active_cubes = set()
inactive_cubes = set()

to_activate = set()
to_deactivate = set()


def analyze_grid():
    """populates sets with inactive and active cubes"""
    global active_cubes, inactive_cubes

    active_cubes = set()
    inactive_cubes = set()

    for space, value in GRID.items():
        if value == '#':
            active_cubes.add(space)
        elif value == '.':
            inactive_cubes.add(space)
        else:  # floor
            continue


def active_around(space) -> int:
    """counts active cubes around (8 ways) selected"""
    x, y = space

    return ((x - 1, y - 1) in active_cubes) \
           + ((x, y - 1) in active_cubes) \
           + ((x + 1, y - 1) in active_cubes) \
           + ((x - 1, y) in active_cubes) \
           + ((x + 1, y) in active_cubes) \
           + ((x - 1, y + 1) in active_cubes) \
           + ((x, y + 1) in active_cubes) \
           + ((x + 1, y + 1) in active_cubes)


def apply_rules(space):
    global to_activate, to_deactivate

    if space in inactive_cubes and active_around(space) == 0:
        to_activate.add(space)
    if space in active_cubes and active_around(space) >= 4:
        to_deactivate.add(space)


def apply_cubes():
    for space in to_activate:
        GRID[space] = '#'
    for space in to_deactivate:
        GRID[space] = 'L'


def pprint_grid(width, length):
    global GRID
    for y in range(length + 1):
        for x in range(width + 1):
            print(GRID[(x, y)], end='')
        print()
    print('-' * 50)


def load_grid(s):
    global GRID
    for y, line in enumerate(s.splitlines()):
        for x, char in enumerate(line):
            GRID[(x, y)] = char
    return x, y


def compute(s: str) -> int:
    global to_activate, to_deactivate
    grid_width, grid_length = load_grid(s)

    while True:
        # pprint_grid(grid_width, grid_length)

        analyze_grid()

        to_activate = set()
        to_deactivate = set()

        for space in GRID:
            apply_rules(space)

        if to_activate or to_deactivate:
            apply_cubes()
        else:
            return len(active_cubes)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 112),
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
