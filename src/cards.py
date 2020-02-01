from collections import namedtuple
import random

SPADES = "S"
HEARTS = "H"
DIAMONDS = "D"
CLUBS = "C"

SUITS = [SPADES, HEARTS, DIAMONDS, CLUBS]

Card = namedtuple("Card", ["suit", "rank"])


class Deck:
    def __init__(self):
        self.cards = []
        for r in SUITS:
            for s in range(1, 14):
                self.cards.append(Card(r, s))
        random.shuffle(self.cards)

    def get_one(self):
        return self.cards.pop()
