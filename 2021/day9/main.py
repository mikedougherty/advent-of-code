import sys


def find_adjacents(m, row, col):
    # above
    if row > 0:
        yield row - 1, col
    # below
    if row < (len(m) - 1):
        yield row + 1, col
    # left
    if col > 0:
        yield row, col - 1
    # right
    if col < (len(m[row]) - 1):
        yield row, col + 1


def find_lowpoints(m):
    lowpoints = []

    for i, row in enumerate(m):
        for j, point in enumerate(row):
            adjacents = list(find_adjacents(m, i, j))
            if all(point < m[row][col] for row, col in adjacents):
                lowpoints.append((i, j))

    return lowpoints


def get_risk_level(m, row, col):
    return m[row][col] + 1


def determine_basin(m, point):
    basin_index = 0
    basin = [point]

    while basin_index != len(basin):
        row, col = basin[basin_index]
        for r, c in find_adjacents(m, row, col):
            if m[r][c] != 9 and (r, c) not in basin:
                basin.append((r, c))

        basin_index += 1

    print(basin)
    return basin


def basin_size(m, b):
    return len(b)


def main(input_file):
    heightmap = []
    for line in input_file.readlines():
        heightmap.append(list(map(int, line.strip())))

    low_points = find_lowpoints(heightmap)
    total_risk = sum(get_risk_level(heightmap, *pt) for pt in low_points)
    print(f"Total risk level: {total_risk}")

    basins = []
    for low_point in low_points:
        basins.append(determine_basin(heightmap, low_point))

    basin_sizes = [basin_size(heightmap, b) for b in basins]
    mult_size = 1
    for bsz in sorted(basin_sizes)[-3:]:
        mult_size *= bsz

    print(f"Top 3 basin sizes multiplied: {mult_size}")


if __name__ == "__main__":
    main(sys.stdin)
