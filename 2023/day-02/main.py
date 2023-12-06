import collections
import sys


class Pick(collections.namedtuple("Pick", ["red", "green", "blue"])):
    @classmethod
    def from_string(cls, string):
        parts = string.split(", ")
        by_color = dict(red=0, green=0, blue=0)
        for part in parts:
            count, color = [x for x in part.split(" ") if x]
            by_color[color] = int(count)

        return cls(**by_color)
    
    def __int__(self):
        return self.red * self.green * self.blue


def main(input_file):
    games = {}
    target = Pick(12, 13, 14)
    for line in input_file.readlines():
        line = line.strip()
        game, picks = line.split(":")
        games[int(game.replace("Game ", ""))] = [Pick.from_string(pick) for pick in picks.split(";")]

    total = 0
    pick_power = 0
    for i, picks in games.items():
        max_pick = Pick(
            max(p.red for p in picks),
            max(p.green for p in picks),
            max(p.blue for p in picks)
        )

        pick_power += int(max_pick)

        if target.red >= max_pick.red and target.green >= max_pick.green and target.blue >= max_pick.blue:
            total += i

    print(total)
    print(pick_power)


if __name__ == "__main__":
    main(sys.stdin)
