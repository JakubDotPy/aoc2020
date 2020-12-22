import argparse
import os.path
import re
from collections import deque
from itertools import count

import pytest

from support.support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
INPUT_S = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


class Card:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Card({self.value})'


class Player:
    def __init__(self, player_id, deck):
        self.player_id = player_id
        self.deck = deque(deck)

    @property
    def score(self):
        return sum(pos * card.value for pos, card in enumerate(reversed(self.deck), start=1))

    @property
    def has_cards(self):
        return bool(self.deck)

    @property
    def deck_str(self):
        return ', '.join(str(card.value) for card in self.deck)

    def play_card(self):
        return self.deck.popleft()

    def take_winning_cards(self, cards):
        self.deck.extend(cards)

    def __repr__(self):
        return f'Player({self.player_id}, {self.deck})'


def compute(s: str) -> int:
    players = []
    for player_group in s.split('\n\n'):
        player_rows = player_group.splitlines()
        player_id = int(re.match(r'\d+', player_rows[1])[0])
        cards = [Card(int(val)) for val in player_rows[1:]]

        players.append(Player(player_id=player_id, deck=cards))

    # PLAY THE GAME
    round_counter = count(start=1)
    while all(player.has_cards for player in players):

        # print(f'-- Round {next(round_counter)} --')
        # print(f'Player 1\'s deck: {players[0].deck_str}')
        # print(f'Player 2\'s deck: {players[1].deck_str}')

        # play the cards
        card_1 = players[0].play_card()
        card_2 = players[1].play_card()

        # print(f'Player 1 plays: {card_1}')
        # print(f'Player 1 plays: {card_2}')

        if card_1.value > card_2.value:
            players[0].take_winning_cards((card_1, card_2))
            # print('Player 1 wins the round!')
        else:
            players[1].take_winning_cards((card_2, card_1))
            # print('Player 2 wins the round!')

        # print()

    return sum(player.score for player in players)  # only the winning player has score


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 306),
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
