import argparse
import os.path
import re
from collections import defaultdict

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
    rules = defaultdict(list)
    rules_s, messages_s = s.split('\n\n')

    # parse rules
    for rule in rules_s.splitlines():
        rule_id_s, conditions = [i.strip() for i in rule.split(':')]

        # get the "a" "b"
        if conditions[1] in 'ab':
            rules[int(rule_id_s)] = conditions[1]
            continue
        else:
            parts = []
            for part in conditions.partition('|'):
                if not part:
                    break
                if part == '|':
                    part = part
                else:
                    part = part.strip()
                parts.append(part)
            rules[int(rule_id_s)] = f"({''.join(parts)})"

    messages = messages_s.splitlines()

    return rules, messages


def compute(s: str) -> int:
    rules, messages = parse(s)

    # replace with the letters I know
    # while there are numbers in rule 0, continue with replacing
    while re.search(r'\d+', rules[0]):
        r_0 = rules[0]
        for n in set(re.findall(r'\d+', r_0)):
            r_0 = re.sub(n, rules[int(n)], r_0)
        r_0 = re.sub(r'\((\w+)\)', r'\1', r_0)
        rules[0] = r_0

    # clean regex
    the_regex = re.sub(' ', '', rules[0])
    while re.search(r'\(\w+\)', the_regex):
        the_regex = re.sub(' ', '', the_regex)
        the_regex = re.sub(r'\((\w+)\)', r'\1', the_regex)

    counts = sum(bool(re.fullmatch(the_regex, message)) for message in messages)

    return counts


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
