import argparse
import os.path
import pprint

import pytest

from support.support import timing

pp = pprint.PrettyPrinter()

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

"""
If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.

If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.

Otherwise, the seat's state does not change.
"""

GRID = dict()
occupied_seats = set()
empty_seats = set()

to_sit = set()
to_leave = set()

grid_width = 0
grid_length = 0


def vec_add(vec1, vec2):
    return vec1[0] + vec2[0], vec1[1] + vec2[1]


def vec_mul(vec, scal):
    return vec[0] * scal, vec[1] * scal


def analyze_grid():
    """populates sets with empty and occupied seats"""
    global occupied_seats, empty_seats

    occupied_seats = set()
    empty_seats = set()

    for seat, value in GRID.items():
        if value == '#':
            occupied_seats.add(seat)
        elif value == 'L':
            empty_seats.add(seat)
        else:  # floor
            continue


def occupied_around(seat) -> int:
    """counts occupied seats around (8 ways) selected"""
    x, y = seat
    occupied = 0

    directions = [
        # x   y
        (-1, -1),  # top \
        (+0, -1),  # top |
        (+1, -1),  # top /

        (-1, -0),  # <-
        (+1, -0),  # ->

        (-1, +1),  # low /
        (+0, +1),  # low |
        (+1, +1),  # low \
        ]
    used_direcitons = set()

    for dist in range(1, max(grid_width, grid_length)):
        # increase distance in all directions

        for direction in directions:

            if direction in used_direcitons:
                continue

            # increase direction
            seat_to_check = vec_add(vec_mul(direction, dist), seat)

            if seat_to_check not in GRID:
                continue  # to next seat

            if GRID[seat_to_check] == '.':
                continue  # to next direction
            if GRID[seat_to_check] == '#':
                occupied += 1
            used_direcitons.add(direction)

    return occupied


def apply_rules(seat):
    global to_sit, to_leave

    if seat in empty_seats and occupied_around(seat) == 0:
        to_sit.add(seat)
    if seat in occupied_seats and occupied_around(seat) >= 5:
        to_leave.add(seat)


def apply_people():
    for seat in to_sit:
        GRID[seat] = '#'
    for seat in to_leave:
        GRID[seat] = 'L'


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
    global to_sit, to_leave, grid_width, grid_length
    grid_width, grid_length = load_grid(s)

    while True:
        # pprint_grid(grid_width, grid_length)

        analyze_grid()

        to_sit = set()
        to_leave = set()

        for seat, value in GRID.items():
            if value != '.':
                apply_rules(seat)

        if to_sit or to_leave:
            apply_people()
        else:
            return len(occupied_seats)


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 26),
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
