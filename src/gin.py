from cards import Deck


class Match:
    SET = 0
    RUN = 1

    def __init__(self, type, cards):
        self.type = type
        self.cards = cards


class Hand:
    def __init__(self, cards):
        self.hand = cards

    def get_best_matches(self):
        """
        Determines best set of matches and calculates unmatched points
        :return: tuple: ( <unmatched points>, [Match, ...] )
        """
        cards = self.hand.copy()
        sets = self.get_sets(cards)
        for m in sets:
            for c in m.cards:
                cards.remove(c)
        runs = self.get_runs(cards)
        sets_first = sets+runs
        set_points = self.calc_unmatched(sets_first)

        cards = self.hand.copy()
        runs = self.get_runs(cards)
        for m in runs:
            for c in m.cards:
                cards.remove(c)
        sets = self.get_sets(cards)
        runs_first = runs+sets
        run_points = self.calc_unmatched(runs_first)
        return (set_points, sets_first) \
            if set_points < run_points \
            else (run_points, runs_first)

    def calc_unmatched(self, matches):
        """
        Calculates unmatched points from unmatched cards
        :param matches: matched sets and runs
        :return: points
        """
        unmatched_points = sum([c.points for c in self.hand])
        for m in matches:
            for c in m.cards:
                unmatched_points -= c.points
        return unmatched_points

    def get_sets(self, cards):
        """
        Generate sets from the given cards
        :param cards:
        :return:
        """
        sets = {}
        for c in cards:
            sets.setdefault(c.rank, []).append(c)
        matches = []
        for rank in sets:
            if len(sets[rank]) >= 3:
                matches.append(Match(Match.SET, sets[rank]))
        return matches

    def get_runs(self, cards):
        by_suit = {}
        for c in cards:
            by_suit.setdefault(c.suit, []).append(c)
            by_suit[c.suit].sort(key=lambda c: c.rank)
        runs = []
        for s in by_suit:
            runs.extend(self._find_runs(by_suit[s],
                                        lambda cards, ca: len(cards) == 0 or ca.rank-1 == cards[-1].rank))
        # runs is a list of lists, convert to Match objects
        return [Match(Match.RUN, cards) for cards in runs]

    def _find_runs(self, cards, predicate):
        runs = []
        self._get_sub(cards, predicate, runs, [], 0)
        return runs

    def _get_sub(self, cards, predicate, all_runs, tmp_run, idx):
        if idx == len(cards):
            if len(tmp_run) >= 3:
                all_runs.append(tmp_run.copy())
            return

        # add next card to list, generate a list with it
        if predicate(tmp_run, cards[idx]):
            tmp_run.append(cards[idx])
            self._get_sub(cards, predicate, all_runs, tmp_run, idx+1)
            tmp_run.pop()
        else:
            if len(tmp_run) >= 3:
                all_runs.append(tmp_run.copy())
            tmp_run = [cards[idx]]
            self._get_sub(cards, predicate, all_runs, tmp_run, idx+1)


if __name__ == "__main__":
    deck = Deck()
    hand = Hand([deck.get_one() for x in range(10)])
    print("Matches")
    for m in hand.get_matches():
        print(m)
