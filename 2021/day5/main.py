import sys


def print_map(m):
    result = ""
    size = (max(k[0] for k in m.keys()), max(k[1] for k in m.keys()))
    for col in range(size[1] + 1):
        for row in range(size[0] + 1):
            point = m[(row, col)]
            if point == 0:
                result += "."
            else:
                result += str(point)
        result += "\n"
    print(result)


def cmp(a, b):
    if a == b:
        return 0
    elif a < b:
        return -1
    else:
        return 1


def points_for_line(start, end, diagonal=True):
    length = max(abs(start[0] - end[0]), abs(start[1] - end[1])) + 1
    x_diff = -1 * cmp(start[0], end[0])
    y_diff = -1 * cmp(start[1], end[1])

    if x_diff and y_diff and not diagonal:
        return

    for i in range(length):
        yield (start[0] + (i * x_diff), start[1] + (i * y_diff))


def main(input_file):
    vents = []
    size = (0, 0)
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        start, end = line.split(" -> ")
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))

        size = (max(size[0], start_x, end_x), max(size[1], start_y, end_y))

        vents.append(((start_x, start_y), (end_x, end_y)))

    m = {}
    for i in range(size[0] + 1):
        for j in range(size[1] + 1):
            m[(i, j)] = 0

    print_map(m)

    for (start, end) in vents:
        points = list(points_for_line(start, end))
        for point in points:
            m[point] += 1

    print_map(m)

    overlaps = sum(1 for v in m.values() if v > 1)
    print(f"There are {overlaps} overlaps")


if __name__ == "__main__":
    main(sys.stdin)
