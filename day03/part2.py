import argparse
import operator
import re
from functools import reduce

import pytest

from support.support import timing

"""Starting at the top-left corner of your map and following a slope of right 3 and down 1,
how many trees would you encounter?

These aren't the only trees, though;
due to something you read about once involving arboreal genetics and biome stability,
the same pattern repeats to the right many times.
"""


# IDEA:
#   Save positions of trees as coords.
#   Use modulo on rows and avoid copying map.


def read_map(map: str) -> (set, int, int):
    """Reads map and return set with tree coords."""
    trees = set()
    for x, row in enumerate(map.splitlines()):
        for y in (m.start() for m in re.finditer('#', row.strip())):
            trees.add((x, y))
    map_height = x
    map_width = len(row.strip())
    return map_height, map_width, trees


def calculate_hits(start_pos, map_height, map_width, trees, slope) -> int:
    step_down, step_right, trees_hit = *slope, 0

    x, y = start_pos
    right_shift = 0
    for _ in range(0, map_height + 1, step_down):
        trees_hit += (x, y) in trees
        right_shift += step_right
        x += step_down
        y = right_shift % map_width
    return trees_hit


def compute(s: str) -> int:
    map_height, map_width, trees = read_map(s)
    start_pos = (0, 0)
    slopes = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1),)
    hits = [calculate_hits(start_pos, map_height, map_width, trees, slope) for slope in slopes]
    return reduce(operator.mul, hits)


INPUT_S = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 336),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
