from unittest import TestCase
from cards import *
from gin import Hand


class TestHand(TestCase):
    def test_get_sets(self):
        cards = [Card(SPADES, 6), Card(DIAMONDS, 6), Card(CLUBS, 6)]
        hand = Hand(cards)
        match = hand.get_sets()
        self.assertEqual(len(match), 1)
        self.assertEqual(cards, match[0].cards)

    def test_get_no_set(self):
        cards = [Card(SPADES, 6), Card(DIAMONDS, 6), Card(CLUBS, 7)]
        match = Hand(cards).get_sets()
        self.assertEqual(len(match), 0)

    def test_multiple_sets(self):
        cards = [Card(SPADES, 6), Card(DIAMONDS, 6), Card(CLUBS, 6),
                 Card(SPADES, 4), Card(SPADES, 1), Card(DIAMONDS, 4),
                 Card(CLUBS, 4), Card(HEARTS, 4)]
        matches = Hand(cards).get_sets()
        self.assertEqual(len(matches), 2)

    def test_four_card_set(self):
        cards = [Card(CLUBS, 2), Card(DIAMONDS, 2), Card(HEARTS, 2), Card(SPADES, 2)]
        matches = Hand(cards).get_sets()
        self.assertEqual(1, len(matches))
        self.assertCountEqual(cards, matches[0].cards)

    def test_get_run(self):
        cards = [Card(SPADES, 1), Card(SPADES, 3), Card(SPADES, 2)]
        matches = Hand(cards).get_runs()
        self.assertEqual(len(matches), 1)
        self.assertCountEqual(cards, matches[0].cards)

    def test_no_runs(self):
        cards = [Card(SPADES, 1), Card(SPADES, 3), Card(SPADES, 5)]
        matches = Hand(cards).get_runs()
        self.assertEqual(len(matches), 0)

    def test_long_run(self):
        cards = [Card(CLUBS, 6), Card(CLUBS, 2), Card(CLUBS, 1),
                 Card(CLUBS, 5), Card(CLUBS, 3), Card(CLUBS, 4)]
        matches = Hand(cards).get_runs()
        self.assertEqual(1, len(matches))
        self.assertCountEqual(cards, matches[0].cards)

    def test_get_run_broken(self):
        cards = [Card(DIAMONDS, 4), Card(DIAMONDS, 7), Card(DIAMONDS, 9),
                 Card(DIAMONDS, 8), Card(DIAMONDS, 11), Card(DIAMONDS, 13)]
        matches = Hand(cards).get_runs()
        self.assertEqual(1, len(matches))
        self.assertCountEqual([Card(DIAMONDS, 7), Card(DIAMONDS, 8), Card(DIAMONDS, 9)],
                              matches[0].cards)

    def test_multiple_runs(self):
        cards = [Card(CLUBS, 1), Card(CLUBS, 5), Card(CLUBS, 2),
                 Card(CLUBS, 6), Card(CLUBS, 3), Card(CLUBS, 7)]
        matches = Hand(cards).get_runs()
        self.assertEqual(2, len(matches))
        for m in matches:
            if (m.cards != [Card(CLUBS, 1), Card(CLUBS, 2), Card(CLUBS, 3)]) \
                    and (m.cards != [Card(CLUBS, 5), Card(CLUBS, 6), Card(CLUBS, 7)]):
                self.fail("Unexpected runs")

    def test_diff_suits(self):
        diamonds = [Card(DIAMONDS, 10), Card(DIAMONDS, 11), Card(DIAMONDS, 12)]
        spades = [Card(SPADES, 4), Card(SPADES, 5), Card(SPADES, 6)]
        clubs = [Card(CLUBS, 8), Card(CLUBS, 3), Card(CLUBS, 11), Card(CLUBS, 7)]
        cards = diamonds + spades + clubs
        random.shuffle(cards)
        matches = Hand(cards).get_runs()
        self.assertEqual(2, len(matches))
        for m in matches:
            if m.cards != diamonds and m.cards != spades:
                self.fail("Match isn't a proper run: {}".format(m.cards))

    def test_unmatched_points_no_matches(self):
        cards = [Card(CLUBS, 1), Card(DIAMONDS, 3), Card(HEARTS, 5), Card(SPADES, 3), Card(CLUBS, 1),
                 Card(DIAMONDS, 11), Card(DIAMONDS, 13), Card(SPADES, 1), Card(HEARTS, 10), Card(HEARTS, 11)]
        expected_points = 54
        points = Hand(cards).calc_unmatched([])
        self.assertEqual(expected_points, points)

    def test_unmatched_points_all_cards_matched(self):
        cards = [Card(CLUBS, 1), Card(CLUBS, 2), Card(CLUBS, 3), Card(CLUBS, 4), Card(CLUBS, 5),
                 Card(CLUBS, 6), Card(CLUBS, 7), Card(CLUBS, 8), Card(CLUBS, 9), Card(CLUBS, 10)]
        random.shuffle(cards)
        hand = Hand(cards)
        matches = hand.get_runs()
        unmatched_points = hand.calc_unmatched(matches)
        self.assertEqual(0, unmatched_points)

    def test_unmatched_points_some_cards_matched(self):
        cards = [Card(DIAMONDS, 1), Card(DIAMONDS, 2), Card(DIAMONDS, 3), Card(DIAMONDS, 6), Card(SPADES, 6),
                 Card(CLUBS, 6), Card(HEARTS, 11), Card(HEARTS, 7), Card(CLUBS, 2), Card(CLUBS, 10)]
        expected_points = 29
        random.shuffle(cards)
        hand = Hand(cards)
        matched = hand.get_runs()
        matched.extend(hand.get_sets())
        points = hand.calc_unmatched(matched)
        self.assertEqual(expected_points, points)
