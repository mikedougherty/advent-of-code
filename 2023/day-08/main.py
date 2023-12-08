import functools
import itertools
import re
import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return (a * b) / gcd(a, b)


def main(input_file):
    directions = None
    locations = {}
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        if directions is None:
            directions = line
            continue
        
        loc, left, right = re.match(r"^(\w+) = \((\w+), (\w+)\)$", line).groups()

        assert loc not in locations
        locations[loc] = (left, right)

    positions = [pos for pos in locations.keys() if pos.endswith('A')]
    first_end = [-1] * len(positions)
    cycle_length = [-1] * len(positions)
    for i, direction in enumerate(itertools.cycle(directions)):
        for j in range(len(positions)):
            positions[j] = locations[positions[j]][direction == 'R']

            if positions[j].endswith('Z'):
                if first_end[j] < 0:
                    first_end[j] = i
                elif (cycle_length[j] < 0) and ((i - first_end[j]) % len(directions) == 0):
                    cycle_length[j] = i - first_end[j]

        if all(cl > 0 for cl in cycle_length):
            break

    print(functools.reduce(lcm, cycle_length, 1))


if __name__ == "__main__":
    main(sys.stdin)
