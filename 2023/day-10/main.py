import sys

def determine_connections(c):
    match c:
        case "|":
            return ((0, -1), (0, 1))
        case "-":
            return ((-1, 0), (1, 0))
        case "L":
            return ((0, -1), (1, 0))
        case "J":
            return ((0, -1), (-1, 0))
        case "7":
            return ((0, 1), (-1, 0))
        case "F":
            return ((0, 1), (1, 0))
        case ".":
            return None
        case "S":
            return "S"

def conn_to_char(conn):
    match conn:
        case ((0, -1), (0, 1)):
            return "|"
        case ((-1, 0), (1, 0)):
            return "-"
        case ((0, -1), (1, 0)):
            return "L"
        case ((0, -1), (-1, 0)):
            return "J"
        case ((0, 1), (-1, 0)):
            return "7"
        case ((0, 1), (1, 0)):
            return "F"
        case "O":
            return "O"
        case "I":
            return "I"
        case None:
            return '.'
        case "^":
            return "^"
        case '_':
            return '_'
        case _:
            raise ValueError(f"Unknown connection: {conn}")

def main(input_file):
    map = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
    
        map.append([determine_connections(c) for c in line])

    start = (-1, -1)
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "S":
                start = (x, y)
                # Entry on X axis:
                if x < len(map) and (-1, 0) in map[y][x + 1]:
                    # East direction has a west connection
                    possible_start_shapes = set(('L', '-', 'F'))
                elif x > 0 and (1, 0) in map[y][x - 1]:
                    # west direction has an east connection
                    possible_start_shapes = set(('J', '-', '7'))
                else:
                    # no connection on X axis
                    possible_start_shapes = set(('|',))
                
                # Entry on Y axis:
                if y < len(map) and map[y + 1][x] is not None and (0, -1) in map[y + 1][x]:
                    # south direction has a north connection
                    possible_start_shapes -= set(('-', 'L', 'J'))
                elif y > 0 and map[y + 1][x] is not None and (0, 1) in map[y - 1][x]:
                    # north direction has a south connection
                    possible_start_shapes -= set(('-', 'F', '7'))
                else:
                    # no connection on Y axis
                    possible_start_shapes = set(('|',))

                assert len(possible_start_shapes) == 1
                map[y][x] = determine_connections(possible_start_shapes.pop())
                break

    visited = set()
    queue = [[start]]
    i = -1
    while queue:
        i += 1
        possible_positions = queue.pop()
        print(f"{i=}, {possible_positions=}")
        nexts = []
        for x, y in possible_positions:
            if (
                (0 > y >= len(map))
                or (0 > x >= len(map[y]))
                or (map[y][x] is None) 
                or ((x, y) in visited)
            ):
                continue

            visited.add((x, y))

            for move in map[y][x]:
                nexts.append((x + move[0], y + move[1]))

        if nexts:
            queue.append(nexts)

    print(i - 1)

    print("part 2")
    pipe = set(visited)

    # Remove all non-visited nodes: junk pipe pieces!
    for y in range(len(map)):
        for x in range(len(map[y])):
            if (x, y) not in visited and map[y][x] is not None:
                map[y][x] = None

    inner = 0
    for y in range(len(map)):
        inside = False
        prev_angle = None

        for x in range(len(map[y])):
            in_pipe = (x, y) in pipe
            ch = conn_to_char(map[y][x])
            if inside:
                inside = not in_pipe or not (ch == '|' or (prev_angle, ch) in (('L', '7'), ('F', 'J')))
            else:
                inside = in_pipe and (ch == '|' or (prev_angle, ch) in (('L', '7'), ('F', 'J')))
            
            if in_pipe and ch in 'L7FJ':
                prev_angle = ch

            if inside and not in_pipe:
                inner += 1
                map[y][x] = 'I'

    for y in range(len(map)):
        line = ''.join(conn_to_char(c) for c in map[y])
        print(line)

    print(f"{inner=}")


if __name__ == "__main__":
    main(sys.stdin)


### attempt at a flood fill sort of algorithm??

    # # Color the edges as "outside" the pipe
    # for x in range(len(map[0])):
    #     if map[0][x] is None:
    #         map[0][x] = 'O'
    #         visited.add((x, 0))
    #     if map[-1][x] is None:
    #         map[-1][x] = 'O'
    #         visited.add((x, len(map) - 1))

    # for y in range(len(map)):
    #     if map[y][0] is None:
    #         map[y][0] = 'O'
    #         visited.add((0, y))
    #     if map[y][-1] is None:
    #         map[y][-1] = 'O'
    #         visited.add((len(map[y]) - y, y))
    
    # # Fill in 'O' by testing adjacency to other O cells.
    # # Quit when we iterate and have not added any new visited cells.
    # start_visited = len(visited)
    # end_visited = 0
    # while start_visited != end_visited:
    #     start_visited = len(visited)
    #     for y in range(len(map)):
    #         for x in range(len(map[y])):
    #             if map[y][x] is not None:
    #                 continue

    #             for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
    #                 if (
    #                     (0 <= (x + adj[0]) < len(map[y]))
    #                     and (0 <= (y + adj[1]) < len(map))
    #                     and (map[y + adj[1]][x + adj[0]] == 'O')
    #                 ):
    #                     map[y][x] = 'O'
    #                     visited.add((x, y))
    #     end_visited = len(visited)

    # start_visited = len(visited)
    # end_visited = 0
    # # Now iterate over all again, for all '.' that have not been visited but are
    # # adjacent to a pipe piece, 'I' piece, or "inner junk", mark them as 'I' and
    # # add them to visited. Mark '_' pieces as '^' for "inner junk".
    # while start_visited != end_visited:
    #     start_visited = len(visited)
    #     for y in range(len(map)):
    #         for x in range(len(map[y])):
    #             if map[y][x] is not None:
    #                 continue
            
    #             for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
    #                 if (
    #                     (0 <= (x + adj[0]) < len(map[y]))
    #                     and (0 <= (y + adj[1]) < len(map))
    #                     and ((map[y + adj[1]][x + adj[0]] in pipe)
    #                          or (map[y + adj[1]][x + adj[0]] in (None, 'I', '^')))
    #                 ):
    #                     if map[y][x] in ('_', None):
    #                         map[y][x] = 'I'
    #                     visited.add((x, y))
    #     end_visited = len(visited)
    #

