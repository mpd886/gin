
import random

SPADES = "S"
HEARTS = "H"
DIAMONDS = "D"
CLUBS = "C"

SUITS = [SPADES, HEARTS, DIAMONDS, CLUBS]


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.points = self.rank if rank <= 10 else 10

    def __eq__(self, other):
        return type(self) == type(other) \
                and self.suit == other.suit \
                and self.rank == other.rank


class Deck:
    def __init__(self):
        self.cards = []
        for s in SUITS:
            for r in range(1, 14):
                self.cards.append(Card(s, r))
        random.shuffle(self.cards)

    def get_one(self):
        return self.cards.pop()
