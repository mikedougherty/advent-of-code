import sys


def find_adjacents(m, row, col):
    # above
    if row > 0:
        yield m[row - 1][col]
    # below
    if row < (len(m) - 1):
        yield m[row + 1][col]
    # left
    if col > 0:
        yield m[row][col - 1]
    # right
    if col < (len(m[row]) - 1):
        yield m[row][col + 1]


def find_lowpoints(m):
    lowpoints = []

    for i, row in enumerate(m):
        for j, point in enumerate(row):
            adjacents = list(find_adjacents(m, i, j))
            if all(point < x for x in adjacents):
                lowpoints.append((i, j))

    return lowpoints


def get_risk_level(m, row, col):
    return m[row][col] + 1


def main(input_file):
    heightmap = []
    for line in input_file.readlines():
        heightmap.append(list(map(int, line.strip())))

    low_points = find_lowpoints(heightmap)

    total_risk = sum(get_risk_level(heightmap, *pt) for pt in low_points)
    print(f"Total risk level: {total_risk}")


if __name__ == "__main__":
    main(sys.stdin)
