import collections
import re
import sys


def parse_crate(level):
    if not level:
        return None, level

    crate_str, level = level[:3], level[4:]
    if crate_str.strip():
        return crate_str[1], level
    else:
        return None, level


def parse_columns(column_input):
    col_ids = list(map(int, column_input.pop().split()))

    columns = collections.defaultdict(list)
    for level in reversed(column_input):
        for col_id in col_ids:
            crate, level = parse_crate(level)
            if crate is not None:
                columns[col_id].append(crate)

    return dict(columns)


def parse_moves(moves_input):
    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    return list(map(lambda x: tuple(map(int, pattern.match(x).groups())), moves_input))


def apply_move(columns, move):
    count, source, dest = move
    ## Part 1:
    # for i in range(count):
    #     columns[dest].append(columns[source].pop())

    # Part 2:
    crates, columns[source] = columns[source][-count:], columns[source][:-count]
    columns[dest].extend(crates)


def main(input_file):
    column_input = []
    moves_input = []

    for line in input_file:
        line = line.rstrip()
        if not line:
            break
        column_input.append(line)

    for line in input_file:
        line = line.rstrip()
        moves_input.append(line)

    columns = parse_columns(column_input)
    moves = parse_moves(moves_input)

    for move in moves:
        apply_move(columns, move)

    top_crates = []
    for k in sorted(columns.keys()):
        top_crates.append(columns[k][-1])

    print("".join(top_crates))


if __name__ == "__main__":
    main(sys.stdin)
