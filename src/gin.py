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

    def get_matches(self):
        pass

    def get_sets(self):
        sets = {}
        for c in self.hand:
            sets.setdefault(c.rank, []).append(c)
        matches = []
        for rank in sets:
            if len(sets[rank]) >= 3:
                matches.append(Match(Match.SET, sets[rank]))
        return matches

    def get_runs(self):
        by_suit = {}
        for c in self.hand:
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
            self._get_sub(cards, predicate, all_runs, tmp_run, idx+1)


if __name__ == "__main__":
    deck = Deck()
    hand = Hand([deck.get_one() for x in range(10)])
    print("Matches")
    for m in hand.get_matches():
        print(m)