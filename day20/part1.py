import argparse
import os.path

import numpy as np
import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""


class Tile:
    def __init__(self, tile_id, matrix):
        self.tile_id = tile_id
        self.matrix = np.array(matrix)

    @property
    def top(self):
        return self.matrix[0]

    @property
    def bottom(self):
        return self.matrix[-1]

    @property
    def left(self):
        return [row[0] for row in self.matrix]

    @property
    def right(self):
        return [row[-1] for row in self.matrix]

    def rotate(self):
        self.matrix = np.rot90(self.matrix)

    def flip_lr(self):
        self.matrix = np.fliplr(self.matrix)

    def flip_ud(self):
        self.matrix = np.flipud(self.matrix)

    def __repr__(self):
        return f'Tile {self.tile_id}'

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.matrix)


def parse(s):
    tiles = []
    for tile in s.split('\n\n'):
        tile_id_s, *tile_matrix = [list(row) for row in tile.splitlines()]
        tiles.append(
            Tile(int(''.join(tile_id_s[5:9])), tile_matrix)
            )
    return tiles


def compute(s: str) -> int:
    tiles = parse(s)
    return 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 20899048083289),
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
