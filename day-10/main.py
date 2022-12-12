import sys

class CRT:
    def __init__(self):
        self.x = [1]

    def addx(self, num):
        self.x.extend([0, int(num)])

    def noop(self):
        self.x.append(0)

    def process(self, instruction, *args):
        getattr(self, instruction)(*args)

    def strength_at_cycle(self, n):
        return sum(self.x[:n])

def main(input_file):
    lines = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    instructions = []
    for line in lines:
        instructions.append(tuple(line.split()))

    crt = CRT()
    for instruction in instructions:
        crt.process(*instruction)

    print(sum(crt.strength_at_cycle(i)*i for i in (20, 60, 100, 140, 180, 220)))

    for y in range(6):
        for x in range(40):
            cycle = (y * 40) + x + 1
            if (x-1) <= crt.strength_at_cycle(cycle) <= (x+1):
                print('#', end='')
            else:
                print('.', end='')
        print()


if __name__ == "__main__":
    main(sys.stdin)
