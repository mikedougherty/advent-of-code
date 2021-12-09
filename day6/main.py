import sys

NUM_DAYS = 80


def main(input_file):
    fishs = list(map(int, input_file.read().split(",")))

    print(f"initial: fish={len(fishs)}")
    for day in range(1, NUM_DAYS + 1):
        new_fish = 0
        for i in range(len(fishs)):
            fishs[i] -= 1
            if fishs[i] < 0:
                fishs[i] = 6
                new_fish += 1

        fishs.extend([8] * new_fish)
        print(f"{day=} fish={len(fishs)}")


if __name__ == "__main__":
    main(sys.stdin)
