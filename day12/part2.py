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

    def __init__(self, initial_position, waypoint_initial_position):
        self.initial_position = np.array(initial_position)
        self.x, self.y = self.initial_position
        self.heading = self.HEADING_VEC[next(self.CARDINAL_DIRECTIONS)]

        self.waypoint_initial_position = np.array(waypoint_initial_position)
        self.w_x, self.w_y = self.waypoint_initial_position

    @property
    def position(self):
        return np.array([self.x, self.y])

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def w_position(self):
        return np.array([self.w_x, self.w_y])

    @w_position.setter
    def w_position(self, value):
        self.w_x, self.w_y = value

    @property
    def manhattan_distance(self):
        return abs(self.x - self.initial_position[0]) \
               + abs(self.y - self.initial_position[1])

    def rotate(self, direction, val):
        if direction == 'L':
            for i in range(val // 90):
                self.w_y, self.w_x = self.w_x, self.w_y
                self.w_x *= -1

        if direction == 'R':
            for i in range(val // 90):
                self.w_y, self.w_x = self.w_x, self.w_y
                self.w_y *= -1

    def process_instruction(self, instruction):
        command, val = instruction[0], instruction[1:]
        val = int(val)

        # movement forward
        if command == 'F':
            self.position += self.w_position * val
            return

        # translation
        if command in self.HEADING_VEC.keys():
            self.w_position += self.HEADING_VEC[command] * val
            return

        # rotation
        if command in 'RL':
            self.rotate(command, val)
            return


def compute(s: str) -> int:
    ship = Ship([0, 0], [10, 1])
    for instruction in s.splitlines():
        ship.process_instruction(instruction)
    return ship.manhattan_distance


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 286),
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
