import argparse
import re

import pytest

from support.support import timing

"""
You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.

"""


def validate_fields(passport):
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', }
    # 'cid' Country ID is optional for now
    return required_fields.issubset(set(passport.keys()))


def validate_year(year, min, max):
    return len(year) == 4 and (min <= int(year) <= max)


def validate_height(height):
    pattern = re.compile(r'(\d+)(\D+)?')
    m = re.match(pattern, height)
    height, units = m.group(1, 2)
    if not units:
        return False
    return (units == 'cm' and (150 <= int(height) <= 193)) \
           or (units == 'in' and (59 <= int(height) <= 76))


def validate_hcl(hcl):
    pattern = re.compile(r'\#[0-9a-f]{6}')
    return bool(re.match(pattern, hcl))


def validate_ecl(ecl):
    return ecl in 'amb blu brn gry grn hzl oth'


def validate_pid(pid):
    pattern = re.compile(r'\d{9}')
    return bool(re.match(pattern, pid))


def validate_passport(passport):
    if not validate_fields(passport):
        return False
    else:
        condition = \
            validate_year(passport['byr'], 1920, 2002) \
            and validate_year(passport['iyr'], 2010, 2020) \
            and validate_year(passport['eyr'], 2020, 2030) \
            and validate_height(passport['hgt']) \
            and validate_hcl(passport['hcl']) \
            and validate_ecl(passport['ecl']) \
            and validate_pid(passport['pid'])

        return condition


def compute(s: str) -> int:
    passports = (dict(param.split(':') for param in passport.split()) for passport in s.split('\n\n'))
    return sum(validate_passport(passport) for passport in passports)


INPUT_S = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 4),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
