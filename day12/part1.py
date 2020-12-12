import argparse
import os.path
from itertools import cycle

import numpy as np
import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
F10
N3
F7
R90
F11"""


class Ship:
    HEADING_VEC = {
        'E': np.array([+1, +0]),
        'S': np.array([+0, -1]),
        'W': np.array([-1, +0]),
        'N': np.array([+0, +1]),
        }

    CARDINAL_DIRECTIONS = cycle(('E', 'S', 'W', 'N'))

    def __init__(self, initial_position):
        self.initial_position = np.array(initial_position)
        self.x, self.y = self.initial_position
        self.heading = self.HEADING_VEC[next(self.CARDINAL_DIRECTIONS)]

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def manhattan_distance(self):
        return abs(self.x - self.initial_position[0]) \
               + abs(self.y - self.initial_position[1])

    def rotate(self, direction, val):
        mul_90 = val // 90

        if direction == 'L':
            mul_90 = 4 - mul_90

        for _ in range(mul_90 - 1):
            next(self.CARDINAL_DIRECTIONS)
        self.heading = self.HEADING_VEC[next(self.CARDINAL_DIRECTIONS)]

    def process_instruction(self, instruction):
        command, val = instruction[0], instruction[1:]
        val = int(val)

        # movement forward
        if command == 'F':
            self.position += self.heading * val
            return

        # translation
        if command in self.HEADING_VEC.keys():
            self.position += self.HEADING_VEC[command] * val
            return

        # rotation
        if command in 'RL':
            self.rotate(command, val)
            return


def compute(s: str) -> int:
    ship = Ship([0, 0])
    for instruction in s.splitlines():
        ship.process_instruction(instruction)
    return ship.manhattan_distance


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 25),
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
