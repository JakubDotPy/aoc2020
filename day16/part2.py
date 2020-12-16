import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

RULE_RE = re.compile(r'^(\D+): ((\d+)-(\d+)) or ((\d+)-(\d+))$')
TICKET_RE = re.compile(r'(\d+,)+\d+$')

RULES = dict()


def check_rule(rule, num):
    """the number satisfies the rule"""
    return any(rng[0] <= num <= rng[1] for rng in rule[1])


def all_numbers_pass(ticket):
    return all([any(check_rule(rule, number) for rule in RULES.items()) for number in ticket])


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

    return rules, tickets


def compute(s: str) -> int:
    global RULES
    RULES, tickets = parse_input(s)

    # my_ticket is first ticket
    my_ticket = tickets[0]

    # filter tickets
    valid_tickets = list(filter(all_numbers_pass, tickets))

    # prepare all possible columns
    col_length = len(valid_tickets[0])
    possible_rules = dict((name, set(range(col_length))) for name in RULES.keys())

    for ticket in valid_tickets:                                 # for every ticket
        for column, number in enumerate(ticket):                 # for numbers at their indexes
            for rule_name, ranges in RULES.items():               # check all the rules
                if not check_rule((rule_name, ranges), number):  # if the number satisfies the rule
                    possible_rules[rule_name].remove(column)     # add its index to possible indexes

    # sort the list ascending by set length
    reduced_names = sorted(list((name, col_set) for name, col_set in possible_rules.items()), key=lambda x: x[1])

    # reduce the columns to find the right ones
    resulting_columns = dict()
    while reduced_names:
        name, prev_column_set = reduced_names.pop(0)
        col_number = prev_column_set.pop()
        resulting_columns[name] = col_number
        reduced_names = [(name, (col_set - {col_number})) for name, col_set in reduced_names]

    # multiply departures
    resulting_multiplication = 1
    for name, column in resulting_columns.items():
        if name.startswith('departure'):
            resulting_multiplication *= my_ticket[column]

    return resulting_multiplication


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
