import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

RULE_RE = re.compile(r'^(\D+): ((\d+)-(\d+)) or ((\d+)-(\d+))$')
TICKET_RE = re.compile(r'(\d+,)+\d+$')


def check_rule(rule, num):
    return any(rng[0] <= num <= rng[1] for rng in rule[1])


def parse_input(s):
    rules = {}
    tickets = []

    for row in s.splitlines():
        # try to find rule
        if m := RULE_RE.fullmatch(row):
            name = m[1]
            rng_1 = int(m[3]), int(m[4])
            rng_2 = int(m[6]), int(m[7])
            rules.update({
                name: [rng_1, rng_2]
                })
        elif TICKET_RE.fullmatch(row):
            tickets.append(list(map(int, row.split(','))))

    my_ticket, tickets = tickets[0], tickets[1:]
    return rules, my_ticket, tickets


def compute(s: str) -> int:
    rules, my_ticket, tickets = parse_input(s)
    tser = 0  # ticket scanning error rate

    for ticket in tickets:
        for number in ticket:
            passed = any(check_rule(rule, number) for rule in rules.items())
            if not passed:
                tser += number

    return tser


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 71),
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
