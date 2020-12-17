import argparse
import os.path
from itertools import count, product

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

    for cube, value in GRID.items():
        if value == '#':
            active_cubes.add(cube)
        elif value == '.':
            inactive_cubes.add(cube)


cubes_around = set(product((-1, 0, 1), repeat=3)) - {(0, 0, 0)}


def active_around(cube) -> int:
    """counts active cubes around (3D) selected"""
    x, y, z = cube

    around = 0
    for s_x, s_y, s_z in cubes_around:
        check = x + s_x, y + s_y, z + s_z
        if check in active_cubes:
            around += 1

    # TODO: return sum((x + mov[0], y + mov[1]) in active_cubes for mov in cubes_around)
    return around


def apply_rules(cube):
    """Applies rules to cube to determine if it will be active or not.

    If a cube is active and exactly 2 or 3 of its neighbors are also active,
     the cube remains active. Otherwise, the cube becomes inactive.

    If a cube is inactive but exactly 3 of its neighbors are active,
     the cube becomes active. Otherwise, the cube remains inactive.
    """
    global to_activate, to_deactivate

    if cube in inactive_cubes and active_around(cube) in (2, 3):
        to_activate.add(cube)
    else:
        to_deactivate.add(cube)

    if cube in inactive_cubes and active_around(cube) == 3:
        to_activate.add(cube)
    else:
        to_deactivate.add(cube)


def apply_cubes():
    for cube in to_activate:
        GRID[cube] = '#'
    for cube in to_deactivate:
        GRID[cube] = '.'


def pprint_grid(width, length):
    global GRID

    layers = sorted(list(set(cube[2] for cube in GRID)))

    for z in layers:
        print(f' layer {z} '.center(20, '-'))
        for y in range(length + 1):
            for x in range(width + 1):
                print(GRID[(x, y, z)], end='')
            print()
    print('=' * 20)


def load_grid(s):
    global GRID
    for y, line in enumerate(s.splitlines()):
        for x, char in enumerate(line):
            GRID[(x, y, 0)] = char  # z coordinate is 0 in the beginning
    return x, y


def compute(s: str) -> int:
    global to_activate, to_deactivate
    grid_width, grid_length = load_grid(s)

    # THE LOOP
    for cycle in count(start=1):
        print(f' cycle {cycle} '.center(30, '#'))
        pprint_grid(grid_width, grid_length)

        analyze_grid()

        to_activate = set()
        to_deactivate = set()

        for cube in GRID:
            apply_rules(cube)

        assert len(to_activate) + len(to_deactivate) == len(GRID)

        if to_activate or to_deactivate:
            apply_cubes()

        # stop condition
        if cycle == 3:
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
