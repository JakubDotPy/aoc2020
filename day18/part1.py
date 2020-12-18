import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
1 + 2 * 3 + 4 * 5 + 6
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""


def get_innermost(expr):
    start, end = 0, len(expr)
    for i, c in enumerate(expr):
        if c == '(':
            start = i
        if c == ')':
            end = i + 1
            break
    return expr[start:end]


def do_math(expr):
    result = 0

    expr = expr[1:-1] if expr.startswith('(') else expr
    epxr_list = re.split(r'(\D)', expr)

    # process first three
    sub_expr_l, epxr_list = epxr_list[:3], epxr_list[3:]
    result += eval(''.join(sub_expr_l))

    while epxr_list:
        # process next two
        sub_expr_l, epxr_list = epxr_list[:2], epxr_list[2:]
        result = eval(str(result) + ''.join(sub_expr_l))

    return result


def process_expression(expr):
    while not expr.isdigit():
        inner = get_innermost(expr)
        inner_result = do_math(inner)
        # put the result instead of the inner expression
        expr = expr.replace(inner, str(inner_result))
    return int(expr)


def compute(s: str) -> int:
    expressions = [line.replace(' ', '') for line in s.splitlines()]
    return sum(process_expression(expr) for expr in expressions)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 26406),
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
