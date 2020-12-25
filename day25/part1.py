import argparse
import os.path

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
5764801
17807724"""


def compute(s: str) -> int:
    card_pk_s, door_pk_s = s.splitlines()
    card_pk = int(card_pk_s)
    door_pk = int(door_pk_s)

    SUBJECT_NUMBER = 7
    REM_DIV = 20201227

    # card loop size
    card_loop_size = 0
    test_num = 1
    while test_num != card_pk:
        test_num *= SUBJECT_NUMBER
        div, rem = divmod(test_num, REM_DIV)
        test_num = rem
        card_loop_size += 1

    # door loop size
    door_loop_size = 0
    test_num = 1
    while test_num != door_pk:
        test_num *= SUBJECT_NUMBER
        div, rem = divmod(test_num, REM_DIV)
        test_num = rem
        door_loop_size += 1

    test_num = 1
    SUBJECT_NUMBER = card_pk
    for _ in range(door_loop_size):
        test_num *= SUBJECT_NUMBER
        div, rem = divmod(test_num, REM_DIV)
        test_num = rem

    return test_num


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 14897079),
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
