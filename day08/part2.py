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
        self.visited = set()
        self.accumulator = 0
        self.cursor = 0
        self.program = program

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

    @property
    def end_condition(self):
        return self.cursor == len(self.program)

    @property
    def infinite_loop(self):
        if self.cursor not in self.visited:
            self.visited.add(self.cursor)
            return False
        else:
            raise RuntimeError('infinite loop')

    def progress(self):
        if not self.infinite_loop:
            # load instruction
            instr, amt = self.program[self.cursor]
            # call the operation
            getattr(self, instr)(amt)

    def run(self):
        while not self.end_condition:
            self.progress()

    def __repr__(self):
        return f'Console(acc={self.accumulator}, cur={self.cursor})'


def parse_program(s):
    return [(instr, int(amt)) for instr, amt in INSTR_RE.findall(s)]


def compute(s: str) -> int:
    program = parse_program(s)

    for i, (instr, amt) in enumerate(program):

        # try to repair program by renaming an instruction
        if instr in ('jmp nop'):
            repaired_program = program.copy()

            instr = 'jmp' if instr == 'nop' else 'nop'  # swap nop<->jmp

            if (instr, amt) == ('jmp', 0): continue  # this would be an infinite loop

            repaired_program[i] = (instr, amt)

            # load the repaired program into console and run it
            console = Console(repaired_program)
            try:
                console.run()
            except RuntimeError:
                continue  # to next repair
            else:
                return console.accumulator


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 8),
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
