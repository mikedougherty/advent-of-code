import collections
import sys

def move(pos, direction):
    vector = dict(
        R=(1, 0),
        L=(-1, 0),
        U=(0, 1),
        D=(0, -1)
    )[direction]

    return (
        pos[0] + vector[0],
        pos[1] + vector[1]
    )

def resolve_tail(head_pos, tail_pos):
    x_diff = head_pos[0] - tail_pos[0]
    y_diff = head_pos[1] - tail_pos[1]

    assert -2 <= x_diff <= 2
    assert -2 <= y_diff <= 2

    x_mag = abs(x_diff)
    # 0 will be 0, else represents 1 or -1 depending on sign
    x_dir = x_mag and (x_diff//x_mag)

    y_mag = abs(y_diff)
    y_dir = y_mag and (y_diff//y_mag)

    if x_mag <= 1 and y_mag <= 1:
        # Don't move. Overlapping or adjacent
        return tail_pos

    if x_mag: # If zero, will not move horizontally
        tail_pos = move(tail_pos, {-1:"L", 1:"R"}[x_dir])
    if y_mag: # If zero, will not move vertically
        tail_pos = move(tail_pos, {-1:"D", 1:"U"}[y_dir])

    return tail_pos


def tail_visits_for_snake(moves, length):
    snake = []
    tail_visits = collections.defaultdict(int)
    for i in range(length):
        snake.append((0,0))

    tail_visits[snake[-1]] += 1
    for direction, mag in moves:
        for i in range(mag):
            snake[0] = move(snake[0], direction)
            for j in range(len(snake)-1):
                snake[j+1] = resolve_tail(snake[j], snake[j+1])
            tail_visits[snake[-1]] += 1

    return len(tail_visits)

def main(input_file):
    moves = []
    for line in input_file.readlines():
        line = line.strip()

        direction, mag = line.split()
        mag = int(mag)
        moves.append((direction, mag))

    print(tail_visits_for_snake(moves, 2))
    print(tail_visits_for_snake(moves, 10))


if __name__ == "__main__":
    main(sys.stdin)
