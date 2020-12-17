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


moves_around = set(product((-1, 0, 1), repeat=4)) - {(0, 0, 0, 0)}


def active_around(cube) -> int:
    """counts active cubes around (3D) selected"""
    x, y, z, w = cube
    return sum((x + mov[0], y + mov[1], z + mov[2], w + mov[3]) in active_cubes for mov in moves_around)


def apply_rules(cube):
    """Applies rules to cube to determine if it will be active or not.

    If a cube is active and exactly 2 or 3 of its neighbors are also active,
     the cube remains active. Otherwise, the cube becomes inactive.

    If a cube is inactive but exactly 3 of its neighbors are active,
     the cube becomes active. Otherwise, the cube remains inactive.
    """
    global to_activate, to_deactivate

    if cube in active_cubes:
        if active_around(cube) in (2, 3):
            to_activate.add(cube)
        else:
            to_deactivate.add(cube)

    if cube in inactive_cubes:
        if active_around(cube) == 3:
            to_activate.add(cube)
        else:
            to_deactivate.add(cube)


def apply_cubes():
    for cube in to_activate:
        GRID[cube] = '#'
    for cube in to_deactivate:
        GRID[cube] = '.'


def pprint_grid():
    """hehehe... 4D... I think not.."""
    global GRID

    width = sorted(list(set(cube[0] for cube in GRID)))
    height = sorted(list(set(cube[1] for cube in GRID)))
    depth = sorted(list(set(cube[2] for cube in GRID)))

    for z in depth:
        print(f' layer {z} '.center(20, '-'))
        for y in height:
            for x in width:
                print(GRID[(x, y, z)], end='')
            print()
    print('=' * 20)


def load_grid(s):
    global GRID

    for y, line in enumerate(s.splitlines()):
        for x, char in enumerate(line):
            GRID[(x, y, 0, 0)] = char  # z and w coordinates are 0 in the beginning


def expand_grid():
    """expands grid to all directions by one"""
    global GRID

    expanded_grid = GRID.copy()

    for x, y, z, w in GRID.keys():
        for m_x, m_y, m_z, m_w in moves_around:
            new_cube = x + m_x, y + m_y, z + m_z, w + m_w
            if new_cube not in GRID:
                expanded_grid[new_cube] = '.'

    GRID = expanded_grid


def compute(s: str) -> int:
    global to_activate, to_deactivate

    load_grid(s)

    # THE LOOP
    for cycle in count(start=1):
        # print(f' cycle {cycle} '.center(30, '#'))
        # pprint_grid()

        expand_grid()
        analyze_grid()  # sets active_cubes and inactive_cubes

        to_activate = set()
        to_deactivate = set()

        for cube in GRID:
            apply_rules(cube)

        if to_activate or to_deactivate:
            apply_cubes()

        # stop condition
        if cycle == 7:
            return len(active_cubes)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 848),
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
