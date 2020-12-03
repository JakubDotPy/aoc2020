import argparse
import re

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


def compute(s: str) -> int:
    start_pos = (0, 0)
    step_down, step_right, trees_hit = 1, 3, 0
    map_height, map_width, trees = read_map(s)

    x, y = start_pos
    right_shift = 0
    for _ in range(0, map_height + 1, step_down):
        trees_hit += (x, y) in trees
        right_shift += step_right
        x += step_down
        y = right_shift % map_width

    return trees_hit


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ("""..##.......
                #...#...#..
                .#....#..#.
                ..#.#...#.#
                .#...##..#.
                ..#.##.....
                .#.#.#....#
                .#........#
                #.##...#...
                #...##....#
                .#..#...#.#""", 7),
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
