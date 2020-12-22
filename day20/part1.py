import argparse
import os.path
from functools import reduce
from operator import mul

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
        self.pos_in_picture = np.array([0, 0])

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

    @property
    def _forward_edges(self):
        edges = [
            self.top,
            self.bottom,
            self.left,
            self.right,
            ]
        return set([''.join(edge) for edge in edges])

    @property
    def _backward_edges(self):
        return set(edge[::-1] for edge in self._forward_edges)

    def match(self, other):
        sides = {
            'top'   : np.array_equal(self.top, other.bottom),
            'bottom': np.array_equal(self.bottom, other.top),
            'left'  : np.array_equal(self.left, other.right),
            'right' : np.array_equal(self.right, other.left),
            }
        return [side for side, result in sides.items() if result]

    def print(self):
        return '\n'.join(''.join(row) for row in self.matrix)

    def __repr__(self):
        return f'Tile {self.tile_id}'

    def __str__(self):
        return f'Tile {self.tile_id}'


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

    # corners match only on two sides!!
    corners = []

    # generate combinations
    for i, this_tile in enumerate(tiles):
        this_tile_edges = set(this_tile._forward_edges)
        for j, other_tile in enumerate(tiles):
            if i == j: continue  # same tile
            for edge in tuple(this_tile_edges):
                if edge in other_tile._forward_edges | other_tile._backward_edges:
                    print(f'{this_tile.tile_id} {other_tile.tile_id}')
                    this_tile_edges.discard(edge)
        if len(this_tile_edges) == 2:  # removing two times (both may be flipped) remaining edges must be 2*2
            corners.append(this_tile.tile_id)

    return reduce(mul, corners)


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
