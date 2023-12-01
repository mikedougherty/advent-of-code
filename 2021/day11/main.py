import functools
import itertools
import sys

MAX_VAL = 9


def increment_all(addresses, octopi):
    for (row, col) in addresses:
        octopi[row][col] += 1


def find_flashers(o):
    results = set()
    for row in range(len(o)):
        for col in range(len(o[row])):
            if o[row][col] > MAX_VAL:
                results.add((row, col))

    return results


@functools.lru_cache
def find_neighbors(o, height, width):
    neighbors = set()
    row, col = o
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if r >= 0 and r < height and c >= 0 and c < width:
                neighbors.add((r, c))

    neighbors.remove(o)
    return neighbors


def print_grid(o):
    for row in range(len(o)):
        for col in range(len(o[row])):
            val = o[row][col]
            if val > MAX_VAL:
                print("*", end="")
            else:
                print(val, end="")
        print()


def main(input_file, iterations):
    octopi = []
    for line in input_file.readlines():
        line = line.strip()
        octopi.append(list(map(int, line)))

    height = len(octopi)
    width = len(octopi[0])
    all_flashed = -1

    print("start:")
    print_grid(octopi)

    total_flashers = 0
    for _ in range(iterations):
        flashers = set()
        flashed = set()
        current_flashers = set()
        new_flashers = set()

        addresses = itertools.product(range(height), range(width))
        increment_all(addresses, octopi)

        round_iterations = 0
        while True:
            current_flashers = find_flashers(octopi)
            new_flashers = current_flashers - flashers
            total_flashers += len(new_flashers)
            flashers |= current_flashers

            round_iterations += 1

            if len(new_flashers) == 0:
                print(
                    f"No new flashers found on sub-iteration {round_iterations}, ending round"
                )
                break

            for flasher in new_flashers:
                increment_all(find_neighbors(flasher, height, width), octopi)

            print(f"Iteration {_}, round={round_iterations}:")
            print_grid(octopi)
            print()

            flashed |= flashers

        for (row, col) in flashed:
            octopi[row][col] = 0

        if len(flashed) == (height * width) and all_flashed == -1:
            all_flashed = _ + 1

        print(
            f"For iteration {_} we had {round_iterations} sub-iterations and {len(flashed)} flashed. Total flashes is now {total_flashers}"
        )
        print_grid(octopi)

    print(f"After {iterations} iterations, {total_flashers} flashes occured")
    print(f"The first time all flashed together was iteration {all_flashed}")
    print_grid(octopi)


if __name__ == "__main__":
    main(sys.stdin, int(sys.argv[1]) if len(sys.argv) > 1 else 100)
