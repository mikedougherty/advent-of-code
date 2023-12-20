import dataclasses
import re
import sys

class Dir:
    DOWN = (0, 1)
    UP = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    @staticmethod
    def from_str(s):
        return {
            'U': Dir.UP,
            'D': Dir.DOWN,
            'R': Dir.RIGHT,
            'L': Dir.LEFT,
        }[s]

@dataclasses.dataclass
class Instruction:
    dir: tuple[int, int]
    mag: int
    color: str

    def __post_init__(self):
        self.dir = Dir.from_str(self.dir)
        self.mag = int(self.mag)

    @classmethod
    def from_part1(cls, s):
        return cls(**re.match(r'(?P<dir>U|D|R|L)\s+(?P<mag>\d+)\s+\(#(?P<color>[a-b0-f]{6})\)$', s).groupdict())

    @classmethod
    def from_part2(cls, s):
        i = cls.from_part1(s)
        return cls('RDLU'[int(i.color[-1])], int(i.color[:-1], 16), '')


# Some evil voodoo magic called a shoestring algorithm :shrug:
def shoestring(plan):
    x, y = 0, 0
    vertices = []
    for i in plan:
        x += i.dir[0] * i.mag
        y += i.dir[1] * i.mag
        vertices.append((x,y))

    fill = 0
    for v1, v2 in zip(vertices[:-1], vertices[1:]+[vertices[0]]):
        fill += v1[0] * v2[1] - v1[1] * v2[0]

    edges = sum(i.mag for i in plan)
    return (fill + edges) // 2 + 1


def main(input_file):
    plan_p1 = []
    plan_p2 = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        plan_p1.append(Instruction.from_part1(line))
        plan_p2.append(Instruction.from_part2(line))

    print(shoestring(plan_p1))
    print(shoestring(plan_p2))

if __name__ == "__main__":
    main(sys.stdin)
