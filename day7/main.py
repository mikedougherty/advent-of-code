import sys


def cost_to_align(x, positions):
    cost = 0
    for p in positions:
        distance = abs(x - p)
        cost += sum(range(1, distance + 1))
    return cost


def main(input_file):
    positions = list(map(int, input_file.read().split(",")))
    possibles = list(range(max(positions)))

    answer, answer_cost = 0, sys.maxsize
    for possible in possibles:
        cost = cost_to_align(possible, positions)
        print(f"Cost to align to {possible}: {cost}")
        if cost < answer_cost:
            answer = possible
            answer_cost = cost

    print(f"Align on position {answer} for cost {answer_cost}")


if __name__ == "__main__":
    main(sys.stdin)
