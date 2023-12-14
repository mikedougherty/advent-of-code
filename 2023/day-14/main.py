import sys

# Convert to a single string for easy comparison
def flatten(grid):
    return ''.join(''.join(l) for l in grid)

# Convert from string to a grid with line length=sz
def inflate(grid, sz):
    return [list(grid[i:i+sz]) for i in range(len(grid)//sz)]

# Rotate 90 degrees and 'tilt'; repeat 4x for a full circle
def cycle(grid):
    for _ in range(4):
        grid = rot90(tilt(grid))
    return grid

# Rotate the grid 90 degrees clockwise -- this is so when we 'tilt'
# the direction iterates through N,W,S,E from a point of reference
# outside the grid
def rot90(grid):
    return list(zip(*grid[::-1]))

# 'tilt' the grid upwards ("north" if not rotated)
def tilt(grid):
    tilted_grid = []
    # transpose it, make a list of strings for easy manipulation
    transposed = list(''.join(l) for l in zip(*grid))
    
    for line in transposed:
        new_chunks = []
        chunks = line.split('#')
        for chunk in chunks:
            new_chunks.append('O' * chunk.count('O') + '.' * chunk.count('.'))
        tilted_grid.append('#'.join(new_chunks))

    # tranpose back
    return list(zip(*tilted_grid))

# Determine "weight" pushing on the top of the grid.
def weight(grid):
    return sum((line.count('O') * (len(grid) - i) for i, line in enumerate(grid)))

def main(input_file):
    grid = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        grid.append(line)

    # Part1
    print(weight(tilt(grid)))

    # Part2
    total_cycles = 1000000000
    cache = {}

    # Find the cycle length
    for i in range(total_cycles):
        key = flatten(grid)
        if key in cache:
            break

        grid = cycle(grid)
        cache[key] = i

    remaining_cycles = (total_cycles - i) % (i - cache[key])

    for _ in range(remaining_cycles):
        grid = cycle(grid)
    
    print(weight(grid))


if __name__ == "__main__":
    main(sys.stdin)
