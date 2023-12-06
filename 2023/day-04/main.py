import dataclasses
import re
import sys
import typing

CARD_RE = re.compile(r'^Card\s+(?P<id>\d+):\s+(?P<correct>(?:\d+\s+)+)\|\s*(?P<answer>(?:\d+\s*)+)+$')

@dataclasses.dataclass
class Card:
    id : int
    correct : typing.List[int]
    answer : typing.List[int]

    @property
    def score(self):
        return int(2 ** (self.correct_count - 1))
    
    @property
    def correct_count(self):
        return sum(a in self.correct for a in self.answer)


def main(input_file):
    cards = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        m = CARD_RE.match(line)
        cards.append(Card(
            int(m.group('id')),
            [int(x) for x in m.group('correct').split()],
            [int(x) for x in m.group('answer').split()],
        ))

    print(sum(c.score for c in cards))
    card_copies = [[card, 1] for card in cards]

    total_cards = 0
    while card_copies:
        card, copies = card_copies.pop(0)
        total_cards += copies
        for i in range(card.correct_count):
            card_copies[i][1] += copies
    
    print(total_cards)
        

if __name__ == "__main__":
    main(sys.stdin)
