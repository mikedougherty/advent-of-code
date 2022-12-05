import sys


def range_contains(a, b):
    return a[0] <= b[0] and a[1] >= b[1]


def range_overlaps(a, b):
    return (a[0] <= b[0] <= a[1]) or (a[0] <= b[1] <= a[1])


def main(input_file):
    range_sets = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        range_set = []
        range_strs = line.split(",")
        for range_str in range_strs:
            range_start, range_end = map(int, range_str.split("-"))
            range_set.append((range_start, range_end))

        range_sets.append(range_set)

    contained = 0
    overlapped = 0
    for (range_a, range_b) in range_sets:
        if range_contains(range_a, range_b) or range_contains(range_b, range_a):
            contained += 1
        if range_overlaps(range_a, range_b) or range_overlaps(range_b, range_a):
            overlapped += 1

    print(contained)
    print(overlapped)


if __name__ == "__main__":
    main(sys.stdin)
