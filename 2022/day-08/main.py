import sys

def is_visible(tree, forest):
    directions = [
        (0, 1),  # down
        (0, -1), # up
        (1, 0),  # right
        (-1, 0), # left
    ]

    vis = False
    scene = 1
    for direction in directions:
        dir_vis, dir_scene = is_visible_direction(direction, tree, forest)
        vis = vis or dir_vis
        scene *= dir_scene

    return vis, scene


def is_visible_direction(direction, tree, forest):
    row, col = tree
    d_y, d_x = direction
    tree_height = forest[row][col]
    vis_distance = 0

    col += d_y
    row += d_x
    while 0 <= row < len(forest) and 0 <= col < len(forest[row]):
        vis_distance += 1
        if forest[row][col] >= tree_height:
            return False, vis_distance

        col += d_y
        row += d_x

    return True, vis_distance


def main(input_file):
    forest = []
    for line in input_file.readlines():
        line = line.strip()
        if not line: continue

        forest.append(list(line))

    visible = []
    best_score = 0

    for i in range(len(forest)):
        for j in range(len(forest[i])):
            tree = (j, i)
            vis, score = is_visible(tree, forest)
            if vis:
                visible.append(tree)

            if score > best_score:
                best_score = score

    print(len(visible), best_score)


if __name__ == "__main__":
    main(sys.stdin)
