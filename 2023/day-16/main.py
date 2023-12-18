import sys

DOWN = (0, 1)
UP = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)


def get_start_vectors(grid, part2=False):
    if not part2:
        return [((0, 0), RIGHT)]

    start_vectors = set()
    for y in range(len(grid)):
        if y == 0:
            # Top left corner, also add 'down'
            start_vectors.add(((0, y), DOWN))
            # Top right, also add 'down'
            start_vectors.add(((len(grid[0]) - 1, y), DOWN))
        if y == len(grid) - 1:
            # Bottom left, also add 'up'
            start_vectors.add(((0, y), UP))
            # Bottom right, also add 'up'
            start_vectors.add(((len(grid[0]) - 1, y), UP))
        # Left edge: add 'right'
        start_vectors.add(((0, y), RIGHT))
        # Right edge: add 'left'
        start_vectors.add(((len(grid[0]) - 1, y), LEFT))

    for x in range(len(grid[0])):
        if x == 0:
            # Top left corner, also add 'right'
            start_vectors.add(((x, 0), RIGHT))
            # Bottom left, also add 'right'
            start_vectors.add(((x, len(grid) - 1), RIGHT))
        if x == len(grid) - 1:
            # Top right, also add 'left'
            start_vectors.add(((x, 0), LEFT))
            # Bottom right, also add 'left'
            start_vectors.add(((x, len(grid) - 1), LEFT))
        # Top edge: add 'down'
        start_vectors.add(((x, 0), DOWN))
        # Bottom edge: add 'up'
        start_vectors.add(((x, len(grid) - 1), UP))

    return start_vectors


def get_energized_count(start_vector, reachability_map):
    visited_vectors = set()
    vectors_to_check = [start_vector]

    while vectors_to_check:
        vector = vectors_to_check.pop(0)
        if vector in visited_vectors:
            continue
        visited_vectors.add(vector)
        vectors_to_check.extend(reachability_map[vector])

    energized_points = set()
    for v in visited_vectors:
        energized_points.add(v[0])

    return len(energized_points)


def build_reachability_map(grid):
    reachability_map = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            for direction in (UP, DOWN, LEFT, RIGHT):
                reachability_map[((x,y), direction)] = adjacent_vectors = set()

                ch = grid[y][x]
                if (
                    ch == '.'
                    or ch == '-' and direction in (RIGHT, LEFT)
                    or ch == '|' and direction in (UP, DOWN)
                ):
                    adjacent_vectors.add(((x + direction[0], y + direction[1]), direction))
                elif ch == '|' and direction in (RIGHT, LEFT):
                    adjacent_vectors.add(((x, y + 1), DOWN))
                    adjacent_vectors.add(((x, y - 1), UP))
                elif ch == '-' and direction in (UP, DOWN):
                    adjacent_vectors.add(((x - 1, y), LEFT))
                    adjacent_vectors.add(((x + 1, y), RIGHT))
                elif ch == '/':
                    if direction == RIGHT:
                        adjacent_vectors.add(((x, y - 1), UP))
                    elif direction == LEFT:
                        adjacent_vectors.add(((x, y + 1), DOWN))
                    elif direction == UP:
                        adjacent_vectors.add(((x + 1, y), RIGHT))
                    elif direction == DOWN:
                        adjacent_vectors.add(((x - 1, y), LEFT))
                elif ch == '\\':
                    if direction == RIGHT:
                        adjacent_vectors.add(((x, y + 1), DOWN))
                    elif direction == LEFT:
                        adjacent_vectors.add(((x, y - 1), UP))
                    elif direction == UP:
                        adjacent_vectors.add(((x - 1, y), LEFT))
                    elif direction == DOWN:
                        adjacent_vectors.add(((x + 1, y), RIGHT))
                else:
                    assert False

                for v in set(adjacent_vectors):
                    i, j = v[0]
                    if (
                        i < 0
                        or j < 0
                        or i >= len(grid[0])
                        or j >= len(grid)
                    ):
                        adjacent_vectors.remove(v)

    return reachability_map

def main(input_file):
    grid = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        grid.append(line)


    reachability_map = build_reachability_map(grid)
    # start_vectors = get_start_vectors(grid, part2=False)
    start_vectors = get_start_vectors(grid, part2=True)
    print(max(get_energized_count(sv, reachability_map) for sv in start_vectors))


if __name__ == "__main__":
    main(sys.stdin)
