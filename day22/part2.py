import argparse
import os.path
import re
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
        self.deck = deck

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
        self.card_played = self.deck.pop(0)
        return self.card_played

    def take_winning_cards(self, cards):
        self.deck.extend(cards)

    def __eq__(self, other):
        return self.player_id == other.player_id

    def __repr__(self):
        return f'Player({self.player_id}, {self.deck})'


def compute(s: str) -> int:
    players = []
    for player_group in s.split('\n\n'):
        player_rows = player_group.splitlines()
        player_id = int(re.findall(r'\d+', player_rows[0])[0])
        cards = [Card(int(val)) for val in player_rows[1:]]

        players.append(Player(player_id=player_id, deck=cards))

    game_counter = count(start=1)

    def play_game(players, game_count):
        """PLAY THE GAME"""

        # print(f'\n=== Game {game_count} ===\n')

        player_1, player_2 = players

        player1s_hands = []
        player2s_hands = []

        round_counter = count(start=1)
        while player_1.has_cards and player_2.has_cards:

            round = next(round_counter)
            # print(f'\n-- Round {round} (Game {game_count}) --')
            # print(f'Player 1\'s deck: {player_1.deck_str}')
            # print(f'Player 2\'s deck: {player_2.deck_str}')

            # IDEA: maybe same hands
            if (player_1.deck in player1s_hands) or (player_2.deck in player2s_hands):
                return player_1
            else:
                player1s_hands.append(player_1.deck.copy())
                player2s_hands.append(player_2.deck.copy())

            # play the cards
            player_1.play_card()
            player_2.play_card()

            # print(f'Player 1 plays: {player_1.card_played}')
            # print(f'Player 2 plays: {player_2.card_played}')

            if player_1.card_played.value <= len(player_1.deck) \
                    and player_2.card_played.value <= len(player_2.deck):
                # print('Playing a sub-game to determine the winner...')
                sub_winner = play_game(
                    (
                        Player(1, deck=player_1.deck[:player_1.card_played.value]),
                        Player(2, deck=player_2.deck[:player_2.card_played.value]),
                        ),
                    next(game_counter)
                    )
                this_winner = next(player for player in players if player == sub_winner)
                this_looser = next(player for player in players if player != sub_winner)
            else:
                if player_1.card_played.value > player_2.card_played.value:
                    this_winner, this_looser = player_1, player_2
                else:
                    this_winner, this_looser = player_2, player_1

            # print(f'{this_winner} wins the round {round} of game {game_count}!')
            this_winner.take_winning_cards((this_winner.card_played, this_looser.card_played))

        winner = next(player for player in players if player.deck)
        # print(f'The winner of game {game_count} is {winner}')
        return winner

    final_winer = play_game(players, next(game_counter))
    return final_winer.score  # only the winning player has score


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 291),
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
