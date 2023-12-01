import sys

class Elf:
    def __init__(self):
        self.calories = 0

    def add_snack(self, calories):
        self.calories += calories


def main(input_file):
    elves = []
    elf = Elf()
    for line in input_file.readlines():
        if line.strip() == '':
            elves.append(elf)
            elf = Elf()
            continue

        elf.add_snack(int(line.strip()))

    elves.sort(key=lambda x: -x.calories)
    print(f"most={elves[0].calories}")
    print(f"top3={sum(x.calories for x in elves[:3])}")



if __name__ == "__main__":
    main(sys.stdin)
