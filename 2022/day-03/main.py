import sys


class Rucksack:
    def __init__(self, s):
        self.contents = s
        self.compartments = s[: (len(s) // 2)], s[(len(s) // 2) :]
        common = set(self.compartments[0]) & set(self.compartments[1])
        assert len(common) == 1
        self.common_item = list(common)[0]

    @property
    def priority(self):
        return item_priority(self.common_item)


def item_priority(item):
    ascii = ord(item)
    if ascii <= ord("Z"):
        return ascii - 38
    else:
        return ascii - 96


def main(input_file):
    groups = []
    group = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        group.append(Rucksack(line))

        if len(group) == 3:
            groups.append(group)
            group = []

    if group:
        groups.append(group)

    badges = []
    for group in groups:
        common = (
            set(group[0].contents) & set(group[1].contents) & set(group[2].contents)
        )
        assert len(common) == 1
        badge = list(common)[0]
        badges.append(badge)

    print(sum(item_priority(b) for b in badges))
    # print(sum(s.priority for s in sacks))


if __name__ == "__main__":
    main(sys.stdin)
