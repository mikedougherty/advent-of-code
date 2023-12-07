import dataclasses
import functools
import sys
import typing

WILDCARDS = ('J',)
## Uncomment for part 1
# WILDCARDS = ()
CARDS = WILDCARDS + tuple(c for c in '23456789TJQKA' if c not in WILDCARDS)
HANDS = ('high', 'one pair', 'two pair', 'three', 'full', 'four', 'five')

@functools.total_ordering
@dataclasses.dataclass
class Card:
    face : str

    def __eq__(self, other):
        return self.face == other.face
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return CARDS.index(self.face) < CARDS.index(other.face)
    
    def __hash__(self):
        return self.face.__hash__()

@functools.total_ordering
@dataclasses.dataclass
class Hand:
    cards : typing.List[Card]
    bid : int

    def __init__(self, cards, bid):
        self.cards = tuple(cards)
        self.bid = bid

    def __eq__(self, other):
        return self.cards == other.cards
    
    def __lt__(self, other):
        if self.strength == other.strength:
            return self.cards < other.cards
        else:
            return HANDS.index(self.strength) < HANDS.index(other.strength)
    
    @property
    def strength(self):
        wildcards = len(list(c for c in self.cards if c.face in WILDCARDS))
        counts = {c: self.cards.count(c) for c in set(self.cards) if c.face not in WILDCARDS}
        high_count = 0
        if counts:
            high_count = max(counts.values())

        if (high_count + wildcards) == 5:
            return 'five'
        elif (high_count + wildcards) == 4:
            return 'four'
        elif (high_count + wildcards) == 3:
            if wildcards == 0:
                if 2 in counts.values():
                    return 'full'
                else:
                    return 'three'
            elif wildcards == 1:
                # two pair promoted to full house
                if high_count == 2 and tuple(counts.values()).count(2) == 2:
                    return 'full'
                else:
                    return 'three'
            elif wildcards == 2:
                # 2 wildcards and 3 other distinct cards (else it would be a 4/5 of a kind)
                return 'three'
        # Don't need to account for wildcard here since any 2-card + wildcard becomes a three
        elif high_count == 2 and (tuple(counts.values()).count(2) == 2):
            return 'two pair'
        elif (high_count + wildcards) == 2:
            return 'one pair'

        return 'high'
    
    @classmethod
    def fromstring(cls, s):
        cards, bid = s.split()
        return cls(map(Card, cards), int(bid))


def main(input_file):
    hands = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
    
        hands.append(Hand.fromstring(line))

    score = 0
    for i, hand in enumerate(sorted(hands)):
        score += ((i+1) * hand.bid)

    print(score)
    

if __name__ == "__main__":
    main(sys.stdin)
