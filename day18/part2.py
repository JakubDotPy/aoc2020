import argparse
import os.path
import re

import pytest

from support.support import timing

"""NOTE:
This solution is insired by Andriamanitra.

I find it very elegant and pythonic.
Since I solved part1 my old way, I used this approach to learn how to bend and better work with number types.

The problem:
Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231

The solution is:

Define my own number class, where
 - addition will stay as usual.         + -> + 
 - multiplication will be addition      * -> +
 - subtraction will be multiplication   - -> *
 
Replace numbers with my new type.
Replace * -> -
replace + -> *

That way, the order of operations for eval will be swapped, 
but the result of operation will be as I want.

For example:
2 * 3 + (4 * 5)
will become
2 - 3 * (4 - 5)

but, * will act as + and - as *

Bracket will be evaluated first, to same result 4 * 5
then, 3 * 20 will be evaluated next but as 3 + 20 to 23
then, 2 - 23 will be evaluated as 2 * 23, same as in original.

Resulting in correct 46
"""

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""


class MyNumber:
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        return MyNumber(self.val + other.val)

    def __sub__(self, other):
        return MyNumber(self.val * other.val)

    def __mul__(self, other):
        return MyNumber(self.val + other.val)

    def __str__(self):
        return str(self.val)


def compute(s: str) -> int:
    s = re.sub(r'(\d+)', r'MyNumber(\1)', s)
    s = s.replace('*', '-')
    s = s.replace('+', '*')

    return sum(eval(line).val for line in s.splitlines())


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 693942),
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
