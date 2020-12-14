import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

WRITE_PATTERN = r'^mem\[(\d+)\] = (\d+)$'


def mask_number(mask, number):
    num_list = list(f'{number:036b}')
    for i, val in enumerate(mask):
        if val != 'X':
            num_list[i] = val
    return int(''.join(num_list), 2)


def compute(s: str) -> int:
    memory = dict()

    groups = s.split('mask = ')
    for group in groups[1:]:
        mask, *mem_writes = group.splitlines()

        for instr in mem_writes:
            m = re.match(WRITE_PATTERN, instr)
            addr, value = m[1], m[2]
            memory[int(addr)] = mask_number(mask, int(value))

    return sum(memory.values())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 165),
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
