import dataclasses
import string
import sys
import typing

Position = tuple[int, int]

def adjacent(label, part):
    adjacent_positions = [
        (part.position[0] - 1, part.position[1] - 1),
        (part.position[0] - 1, part.position[1]),
        (part.position[0] - 1, part.position[1] + 1),
        (part.position[0], part.position[1] - 1),
        (part.position[0], part.position[1] + 1),
        (part.position[0] + 1, part.position[1] - 1),
        (part.position[0] + 1, part.position[1]),
        (part.position[0] + 1, part.position[1] + 1),
    ]

    return any(pos in label.positions for pos in adjacent_positions)


@dataclasses.dataclass
class PartLabel:
    i : int
    positions : typing.List[Position]

    def __init__(self, i, positions):
        self.i = i
        self.positions = positions


@dataclasses.dataclass
class Part:
    ch : str
    position : Position

    def __init__(self, ch, pos):
        self.ch = ch
        self.position = pos

@dataclasses.dataclass
class Gear:
    label1 : PartLabel
    label2 : PartLabel

    @property
    def ratio(self) -> int:
        return self.label1.i * self.label2.i


def main(input_file):
    row = -1
    labels = []
    parts = []
    for line in input_file.readlines():
        row += 1
        line = line.strip()
        if not line:
            continue

        label = None
        label_positions = []
        col = -1
        while line:
            col += 1
            ch, line = line[0], line[1:]

            if ch in string.digits:
                label_positions.append((col, row))
                if label is None:
                    label = ''
                label += ch
                continue
            elif label is not None:
                # Encountered a part or a blank space, so we're done with the label
                labels.append(PartLabel(int(label), label_positions))
                label = None
                label_positions = []

            if ch == '.':
                continue
            
            parts.append(Part(ch, (col, row)))

        # Done with the line, if we have a label, add it
        if label is not None:
            labels.append(PartLabel(int(label), label_positions))

    total = 0
    gears = []
    for part in parts:
        adjacent_labels = []
        for label in list(labels):
            if adjacent(label, part):
                total += label.i
                adjacent_labels.append(label)

        if part.ch == '*' and len(adjacent_labels) == 2:
            gears.append(Gear(*adjacent_labels))

    print(total)
    print(sum(g.ratio for g in gears))


if __name__ == "__main__":
    main(sys.stdin)
