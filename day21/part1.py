import argparse
import os.path
from collections import defaultdict
from itertools import count

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


class Food:
    c = count(start=1)
    allergens_to_ingredient = defaultdict(set)

    def __init__(self, row):
        self.food_id = next(Food.c)
        self.ingredients, self.allergens = self.parse(row)

    def parse(self, row):
        ingr_s, _, aller_s = row.partition(' (contains ')
        ingredients = set(ingr_s.split())
        allergens = set(aller_s[:-1].split(', '))

        for allergen in allergens:
            Food.allergens_to_ingredient[allergen].update(ingredients)

        return ingredients, allergens

    def __repr__(self):
        return f'Food no.{self.food_id}'


def compute(s: str) -> int:
    dishes = [Food(row) for row in s.splitlines()]

    all_ingredients = set(ingredient for food in dishes for ingredient in food.ingredients)

    # reduce ingredients and their allergens:
    # sort the list ascending by set length
    reduced_dishes = sorted(list(
        (ingred, allerg) for ingred, allerg in Food.allergens_to_ingredient.items()
        ), key=lambda x: x[1])

    safe_ingredients = []
    # reduce the columns to find the right ones
    while reduced_dishes:
        ingredient, allergens_set = reduced_dishes.pop(0)
        if not allergens_set:
            safe_ingredients.append(ingredient)
            continue

        to_remove = allergens_set.pop()
        reduced_dishes = [(ingredient, (allergens_set - {to_remove})) for ingredient, allergens_set in reduced_dishes]

    return


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 5),
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
