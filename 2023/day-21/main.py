import sys

DOWN = (0, 1)
UP = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)


def possible_endpoints(grid, positions, steps):
    if steps == 0:
        return positions

    next = set()
    for pos in positions:
        for direction in (UP, DOWN, LEFT, RIGHT):
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])

            if grid[new_pos[1] % len(grid)][new_pos[0] % len(grid[0])] == '#':
                continue

            next.add(new_pos)

    return possible_endpoints(grid, next, steps - 1)


def main(input_file):
    grid = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        grid.append(list(line))

    start_pos = (-1, -1)
    for j, row in enumerate(grid):
        if 'S' in row:
            start_pos = (j, row.index('S'))
            break

    print(len(possible_endpoints(grid, [start_pos], steps=64)))

    ## Some facts about the input data:
    ## The size is 131,131 (square)
    ## The start point is 65,65, which is the center point! This becomes important.
    ## The column and row that the start point is in, does not have any obstacles
    ##
    ## So, we will reach the end of our grid in 65 steps no matter which direction we go,
    ## then the map loops. (note: based on this information, part1 is specifically
    ## designed to not loop!)
    ##
    ## Let's calculate how many squares we get from running the same part1 algorithm after 65 steps,
    ## then 2 grids worth of steps (131+65) and 3 grids worth of steps (131+131+65)
    ## Use these datapoints to solve a quadratic equation that we can extrapolate to the requested
    ## large number `26501365`.
    ## note: (26501365 - 65)/131 = 202300 (aka, 100 * CURRENT_YEAR) :)
    sz = len(grid)
    assert len(grid[0]) == sz

    datapoints = [len(possible_endpoints(grid, [start_pos], steps=start_pos[0] + i * sz)) for i in range(3)]

    num_steps = 26501365

    # Doin some quadratic formula factoring, stolen
    # x1, x2, x3 = 65, 196, 327
    y1, y2, y3 = datapoints
    a = (y3 - (2*y2) + y1) // 2
    b = y2 - y1 - a
    c = y1

    ## Use factors to calculate any number of grids worth of steps
    f = lambda n: (a * n**2) + (b * n) + c
    assert f(0) == y1
    assert f(1) == y2
    assert f(2) == y3

    # How many grids do we traverse with our `num_steps`?
    grid_repeats = (num_steps - start_pos[0]) // sz
    # Use our quadratic formula to calculate the number of possible squares to visit (puzzle answer)
    print(f(grid_repeats))

if __name__ == "__main__":
    main(sys.stdin)
