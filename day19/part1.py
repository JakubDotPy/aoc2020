import argparse
import os.path
import re

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


def parse(s):
    rules = dict()
    rules_s, messages_s = s.split('\n\n')

    # parse rules
    for rule in rules_s.splitlines():
        id_s, _, rule_s = rule.partition(': ')
        rules[id_s] = rule_s

    messages = messages_s.splitlines()

    return rules, messages


def compute(s: str) -> int:
    rules, messages = parse(s)

    def part_re(id_s):
        """recursive"""
        if id_s == '|': return '|'

        rule_s = rules[id_s]
        if rule_s.startswith('"'):
            return rule_s[1]
        else:
            return f"({''.join(part_re(p_id_s) for p_id_s in rule_s.split())})"

    pattern = re.compile(part_re('0'))
    return sum(bool(re.fullmatch(pattern, message)) for message in messages)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 2),
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
