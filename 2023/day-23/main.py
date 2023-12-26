import dataclasses
import sys
import typing

@dataclasses.dataclass
class Hike:
    path: list[(int, int)]


def get_possible_moves(hike: Hike, grid: list[list[str]]) -> list[(int, int)]:
    x, y = hike.path[-1]
    moves = []
    if grid[y][x] in '>v<^':
        return {
            '>': [(x + 1, y)],
            '<': [(x - 1, y)],
            'v': [(x, y + 1)],
            '^': [(x, y - 1)],
        }[grid[y][x]]
    else:
        for point in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if point in hike.path:
                continue
            if grid[point[1]][point[0]] != '#':
                moves.append(point)
        return moves


def main(input_file):
    grid = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        grid.append(list(line))

    start_point = (grid[0].index('.'), 0)
    end_point = (grid[-1].index('.'), len(grid) - 1)

    hikes = [Hike([start_point])]

    finished_hikes = []
    while hikes:
        print(len(hikes))
        hike = hikes.pop()
        while hike.path[-1] != end_point:
            possible_moves = get_possible_moves(hike, grid)
            if len(possible_moves) == 0:
                # This hike is a dead end
                break

            # Add the first possibility to this hike
            hike.path.append(possible_moves[0])
            if len(possible_moves) > 1:
                # Multiple possible moves, so create new hikes
                for move in possible_moves[1:]:
                    hikes.append(Hike(hike.path[:-1] + [move]))

        if hike.path[-1] == end_point:
            finished_hikes.append(hike)

    print(len(finished_hikes))
    print(max(len(hike.path) for hike in finished_hikes))


if __name__ == "__main__":
    main(sys.stdin)
