import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""
INSTR_RE = re.compile(r'(\w+) ([+-]\d+)')


class Console:

    def __init__(self, program):
        self.program = program
        self.accumulator = 0
        self.cursor = 0

    def acc(self, amount):
        """increases the accumulator by given amount"""
        self.accumulator += amount
        self.cursor += 1

    def jmp(self, offset):
        """moves the cursor by given offset"""
        self.cursor += offset

    def nop(self, offset):
        """no operation

        does nothing, but moves cursor by one position"""
        self.cursor += 1

    # try this as an iterator
    def __iter__(self):
        return self

    def __next__(self):
        instr, amt = self.program[self.cursor]
        # call the operation
        getattr(self, instr)(amt)

    def __repr__(self):
        return f'Console(acc={self.accumulator}, cur={self.cursor})'


def parse_program(s):
    return [(instr, int(amt)) for instr, amt in INSTR_RE.findall(s)]


def compute(s: str) -> int:
    program = parse_program(s)
    console = Console(program)

    visited_instr = set()
    while console.cursor not in visited_instr:
        visited_instr.add(console.cursor)
        next(console)

    return console.accumulator


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 5),
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
