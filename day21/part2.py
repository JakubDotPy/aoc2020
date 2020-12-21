import argparse
import os.path
from functools import reduce
from itertools import count
from operator import and_

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


# safe kfcds, nhms, sbzzf, trh


class Food:
    c = count(start=1)
    all_alergens = set()
    all_ingredients = set()

    def __init__(self, row):
        self.food_id = next(Food.c)
        self.ingredients, self.allergens = self.parse(row)
        self.allergen_to_ingredient = {
            allergen: self.ingredients
            for allergen in self.allergens
            }

    def parse(self, row):
        ingr_s, _, aller_s = row.partition(' (contains ')
        ingredients = set(ingr_s.split())
        allergens = set(aller_s[:-1].split(', '))

        Food.all_alergens.update(allergens)
        Food.all_ingredients.update(ingredients)

        return ingredients, allergens

    def __repr__(self):
        return f'Food no.{self.food_id}'


def compute(s: str) -> int:
    dishes = [Food(row) for row in s.splitlines()]

    possible_allergens = dict()
    for ingredient in Food.all_alergens:
        possible_allergens[ingredient] = \
            reduce(and_, [dish.allergen_to_ingredient.get(ingredient, dish.all_ingredients) for dish in dishes])

    # sort the list ascending by set length
    reduced_allergens = sorted(list(
        (name, ingred_set) for name, ingred_set in possible_allergens.items()),
        key=lambda x: len(x[1])
        )

    # reduce the columns to find the right ones
    resulting_allergens = dict()
    while reduced_allergens:
        name, prev_allergen_set = reduced_allergens.pop(0)
        ingredient = prev_allergen_set.pop()
        resulting_allergens[name] = ingredient
        reduced_allergens = sorted([(name, (col_set - {ingredient})) for name, col_set in reduced_allergens],
                                   key=lambda x: len(x[1])
                                   )
    # canonical dangerous ingredient list
    cdil = ','.join(resulting_allergens[k] for k in sorted(resulting_allergens.keys()))

    return cdil


@pytest.mark.solved
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
