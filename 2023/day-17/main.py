import itertools
import math
import sys

DOWN = (0, 1)
UP = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)


def navigate(grid, min_mv, max_mv):
    max_y = len(grid) - 1
    max_x = len(grid[0]) -1

    start = (0, 0)
    end = (max_x, max_y)

    visited = set()
    to_check = [(0, start, RIGHT), (0, start, DOWN)]

    cost = 0
    iterations = 0
    while to_check:
        iterations += 1
        if iterations % 1000 == 0:
            # dummy progress meter :shrug:
            print(len(to_check))

        to_check.sort(reverse=True)
        cost, (x, y), direction = to_check.pop()

        if (x, y) == end:
            return cost

        if ((x, y), direction) in visited:
            continue

        visited.add(((x, y), direction))
        start_cost = cost
        next_x, next_y = x, y

        cost = start_cost
        for i in range(max_mv):
            # Travel 'i' tiles in the current direction
            next_x, next_y = x + direction[0] * (i+1), y + direction[1] * (i+1)

            if next_x < 0 or next_y < 0 or next_x > max_x or next_y > max_y:
                # Out of bounds
                break

            # How much does it cost to go to that tile?
            # (accumulates across iterations of this loop)
            cost += grid[next_y][next_x]

            # Haven't traveled far enough to be able to turn, so don't
            # add perpendicular neighbors
            if (i+1) < min_mv:
                continue

            # We CAN turn, so queue neighbors on our perpendicular axis with
            # a new direction if they haven't been visited yet.
            if direction in (UP, DOWN):
                if ((next_x, next_y), LEFT) not in visited:
                    to_check.append((cost, (next_x, next_y), LEFT))
                if ((next_x, next_y), RIGHT) not in visited:
                    to_check.append((cost, (next_x, next_y), RIGHT))
            if direction in (LEFT, RIGHT):
                if ((next_x, next_y), UP) not in visited:
                    to_check.append((cost, (next_x, next_y), UP))
                if ((next_x, next_y), DOWN) not in visited:
                    to_check.append((cost, (next_x, next_y), DOWN))

    return cost


def main(input_file):
    grid = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        grid.append([int(ch) for x in line.split() for ch in x])

    print("--> answer pt1", navigate(grid, min_mv=1, max_mv=3))
    print("--> answer pt2", navigate(grid, min_mv=4, max_mv=10))

if __name__ == "__main__":
    main(sys.stdin)
