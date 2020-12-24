import argparse
import os.path
import re
from collections import Counter

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


def compute(s: str) -> int:
    paths = [re.findall(DIRECTIONS_RE, row) for row in s.splitlines()]

    black_tiles = set()

    dir_to_xy = {
        'e' : (1, 0),
        'se': (0, -1),
        'sw': (-1, -1),
        'w' : (-1, 0),
        'nw': (0, 1),
        'ne': (1, 1),
        }

    for path in paths:
        x, y = 0, 0

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

        for direction in final_moves:
            x, y = x + direction[0], y + direction[1]
        final_pos = (x, y)
        if final_pos in black_tiles:
            black_tiles.discard(final_pos)  # turn white
        black_tiles.add(final_pos)

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
