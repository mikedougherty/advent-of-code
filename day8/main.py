import sys

DIGITS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

TARGETS = [1, 4, 7, 8]


def main(input_file):
    entries = [
        tuple(x.split() for x in line.split(" | ", 1))
        for line in input_file.readlines()
    ]

    hits = 0
    for entry in entries:
        for target in TARGETS:
            for output in entry[1]:
                if len(output) == len(DIGITS[target]):
                    hits += 1

    print(f"Detected {hits} instances of {TARGETS}")


if __name__ == "__main__":
    main(sys.stdin)
