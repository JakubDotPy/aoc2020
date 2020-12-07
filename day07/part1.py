import argparse
import os.path
import re
from collections import defaultdict

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_STR = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

PARENT_re = re.compile(r'^(?P<parent>\w+ \w+)(?P<rest>.*)')
BAG_re = re.compile(r'(\d+) (\w+ \w+)')


def parse_bags(s):
    structure = defaultdict(list)
    for line in s.splitlines():
        match = PARENT_re.match(line)
        parent = match['parent']
        children = [(int(num), color) for num, color in BAG_re.findall(match['rest'])]
        for count, color in children:
            structure[color].append(parent)
    return structure


def compute(s: str) -> int:
    target = 'shiny gold'
    structure = parse_bags(s)

    paths_to_target = set()
    pool = structure[target]

    # traverse
    while pool:
        color = pool.pop()
        if color not in paths_to_target:
            paths_to_target.add(color)
            pool.extend(structure[color])

    return len(paths_to_target)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_STR, 4),
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
