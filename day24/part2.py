import argparse
import os.path
import re
from collections import Counter
from functools import reduce

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

"""
  ne / \ nw
   e|   | w
  se \ / sw
"""

DIRECTIONS_RE = re.compile(r'(e|se|sw|w|nw|ne)')

dir_to_xy = {
    'e' : (1, 0),
    'se': (0, -1),
    'sw': (-1, -1),
    'w' : (-1, 0),
    'nw': (-1, 1),
    'ne': (0, 1),
    }

black_tiles = set()
white_tiles = set()

to_black = set()
to_white = set()

tuple_sum = lambda a, b: (a[0] + b[0], a[1] + b[1])


def load_blacks(paths):
    for path in paths:

        # reduce path using counter
        min_path = Counter(path)
        sw_ne = min_path['sw'] - min_path['ne']
        w_e = min_path['w'] - min_path['e']
        nw_se = min_path['nw'] - min_path['se']

        final_moves = []
        if sw_ne < 0:
            final_moves.append(tuple(abs(sw_ne) * coord for coord in dir_to_xy['ne']))
        else:
            final_moves.append(tuple(abs(sw_ne) * coord for coord in dir_to_xy['sw']))

        if w_e < 0:
            final_moves.append(tuple(abs(w_e) * coord for coord in dir_to_xy['e']))
        else:
            final_moves.append(tuple(abs(w_e) * coord for coord in dir_to_xy['w']))

        if nw_se < 0:
            final_moves.append(tuple(abs(nw_se) * coord for coord in dir_to_xy['se']))
        else:
            final_moves.append(tuple(abs(nw_se) * coord for coord in dir_to_xy['nw']))

        final_pos = reduce(tuple_sum, final_moves)

        if final_pos in black_tiles:
            black_tiles.discard(final_pos)  # turn white
            continue
        black_tiles.add(final_pos)


def generate_around(tile):
    for dif in dir_to_xy.values():
        yield tuple_sum(tile, dif)


def black_around(tile):
    around = generate_around(tile)

    total_around = 0
    for diff in around:
        that_tile = tuple_sum(diff, tile)
        if that_tile in black_tiles:
            total_around += 1
        else:
            white_tiles.add(that_tile)

    return total_around


def apply_changes():
    global black_tiles, white_tiles

    black_tiles.union(to_black)
    black_tiles.difference_update(to_white)

    white_tiles.union(to_white)
    white_tiles.difference_update(to_black)


def compute(s: str) -> int:
    paths = [re.findall(DIRECTIONS_RE, row) for row in s.splitlines()]

    load_blacks(paths)

    for day in range(1, 100 + 1):

        to_white = set()
        to_black = set()

        # analyze blacks
        for tile in black_tiles:
            num_around = black_around(tile)
            if num_around == 0 or num_around > 2:
                to_white.add(tile)

        for tile in white_tiles:
            num_around = black_around(tile)
            if num_around == 2:
                to_black.add(tile)

        apply_changes()

        print(f'Day {day} tiles {len(black_tiles)}')

    return len(black_tiles)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 10),
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
