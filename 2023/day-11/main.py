import sys


def main(input_file):
    grid = []
    for line in input_file:
        line = line.strip()
        if not line:
            continue
        grid.append(list(line))

    # Has empty lines/columns multiplied by 2
    expanded_grid = []
    for line in grid:
        expanded_grid.append(line)
        if set(line) == set('.'):
            expanded_grid.append(list(line))
    
    # transpose:
    expanded_grid = list(zip(*expanded_grid))
    h_growth = 0
    for x in range(len(expanded_grid)):
        if set(expanded_grid[x + h_growth]) == set('.'):
            expanded_grid.insert(x + h_growth, ['.'] * len(expanded_grid[0]))
            h_growth += 1

    galaxies = []
    for y in range(len(expanded_grid)):
        for x in range(len(expanded_grid[y])):
            if expanded_grid[y][x] == '#':
                galaxies.append((x, y))

    pairs = {}
    for g1 in galaxies:
        for g2 in galaxies:
            if g1 == g2 or (g2, g1) in pairs:
                continue

            pairs[(g1, g2)] = (max(g1[0], g2[0]) - min(g1[0], g2[0])) + (max(g1[1], g2[1]) - min(g1[1], g2[1]))

    print(sum(pairs.values()))

    #--- Part 2

    # Using original grid, instead of adding to it, replace empty lines/cols with '*'
    # to symbolize "lightyears"
    for line in grid:
        if set(line) == set('.'):
            line[:] = ['*'] * len(line)

    grid = list(zip(*grid))
    for i in range(len(grid)):
        grid[i] = list(grid[i])
        if set(grid[i]) <= set('.*'):
            grid[i][:] = ['*'] * len(grid[i])

    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '#':
                galaxies.append((x, y))

    pairs = {}
    total = 0
    for g1 in galaxies:
        for g2 in galaxies:
            if g1 == g2 or (g2, g1) in pairs:
                continue

            delta_x = list(grid[0][min(g1[0], g2[0]):max(g1[0], g2[0])])
            delta_y = list(x[0] for x in grid[min(g1[1], g2[1]):max(g1[1], g2[1])])

            lightyears_x = delta_x.count('*')
            lightyears_y = delta_y.count('*')
            
            short_x = len(delta_x) - lightyears_x
            short_y = len(delta_y) - lightyears_y

            dist = (short_x + short_y) + ((lightyears_x + lightyears_y) * 100)
            pairs[(g1, g2)] = dist
            
            total += dist

    print(total)

if __name__ == "__main__":
    main(sys.stdin)
