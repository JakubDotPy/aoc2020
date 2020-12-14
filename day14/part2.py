import argparse
import os.path
import re
from itertools import product

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

WRITE_PATTERN = r'^mem\[(\d+)\] = (\d+)$'


def decode_addresses(mask, addr):
    addresses = set()

    floating_addr = list(f'{addr:036b}')
    for i, val in enumerate(mask):
        if val == '0':
            continue
        else:
            floating_addr[i] = val

    num_x = sum(bit == 'X' for bit in floating_addr)
    for replacement in [i for i in product('10', repeat=num_x)]:
        floating_addr_repl = floating_addr.copy()
        replacement = list(replacement)
        for i, bit in enumerate(floating_addr_repl):
            if bit == 'X':
                floating_addr_repl[i] = replacement.pop(0)
        addresses.add(int(''.join(floating_addr_repl), 2))

    return addresses


def compute(s: str) -> int:
    memory = dict()

    groups = s.split('mask = ')
    for group in groups[1:]:
        mask, *mem_writes = group.splitlines()

        for instr in mem_writes:
            m = re.match(WRITE_PATTERN, instr)
            addr, value = m[1], m[2]
            addresses = decode_addresses(mask, int(addr))
            for addr in addresses:
                memory[addr] = int(value)

    return sum(memory.values())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 208),
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
