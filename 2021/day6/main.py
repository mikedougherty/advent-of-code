import sys

NUM_DAYS = 256
REPRO_AGE = 2
GEST_PERIOD = 7


def main(input_file):
    fish_phases = [0] * (REPRO_AGE + GEST_PERIOD)
    for fish in list(int(x) for x in input_file.read().split(",")):
        fish_phases[REPRO_AGE + (GEST_PERIOD - fish) - 1] += 1

    print(f"initial: fish={sum(fish_phases)}, {fish_phases=}")
    for day in range(1, NUM_DAYS + 1):
        new_fish = fish_phases.pop()
        fish_phases.insert(0, new_fish)
        fish_phases[REPRO_AGE] += new_fish

        print(f"{day=} fish={sum(fish_phases)}, {fish_phases=}")


if __name__ == "__main__":
    main(sys.stdin)
