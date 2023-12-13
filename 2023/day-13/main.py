import sys

def diff_score(a_lines, b_lines):
    a = '\n'.join(''.join(x) for x in a_lines)
    b = '\n'.join(''.join(x) for x in b_lines)

    return sum(ch_a != ch_b for ch_a, ch_b in zip(a, b))

def get_reflection_score(grid, score_factor=1, smudges=0):
    for reflection_sz in range((len(grid)//2) + 1, 0, -1):
        for y in range((len(grid) - (2*reflection_sz)) + 1):
            before_junk = grid[:y]
            first_half = grid[y : y + reflection_sz]
            second_half = grid[y + reflection_sz : y + (2*reflection_sz)]
            after_junk = grid[y + (2*reflection_sz):]

            if before_junk and after_junk:
                continue

            if diff_score(first_half, second_half[::-1]) == smudges:
                return (y+reflection_sz) * score_factor
    
    if score_factor == 100:
        return 0

    return get_reflection_score(list(zip(*grid)), 100, smudges)


def main(input_file):
    grids = []
    cur_grid = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            if cur_grid:
                grids.append(cur_grid)
                cur_grid = []
            continue

        cur_grid.append(line)

    if cur_grid:
        grids.append(cur_grid)
    
    clean_score = 0
    smudge_score = 0
    for grid in grids:
        clean_score += get_reflection_score(list(zip(*grid)), smudges=0)
        smudge_score += get_reflection_score(list(zip(*grid)), smudges=1)

    print(clean_score)
    print(smudge_score)


if __name__ == "__main__":
    main(sys.stdin)
