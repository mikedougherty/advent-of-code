import sys


def score(opp_move, my_move):
    play_score = dict(a=1, b=2, c=3)
    opp_score = play_score[opp_move]
    my_score = play_score[my_move]

    if opp_move == my_move:
        # Draw
        opp_score += 3
        my_score += 3
    elif (
        (opp_move == "a" and my_move == "b")
        or (opp_move == "b" and my_move == "c")
        or (opp_move == "c" and my_move == "a")
    ):
        # i win
        my_score += 6
    else:
        # i lose
        opp_score += 6

    return opp_score, my_score


def move_for_outcome(opp_move, outcome):
    # draw
    if outcome == "y":
        # draw
        return opp_move

    if outcome == "x":
        # lose
        return dict(
            a="c",
            b="a",
            c="b",
        )[opp_move]

    # win
    return dict(
        a="b",
        b="c",
        c="a",
    )[opp_move]


def simulate(guide, decoder):
    opp_score, my_score = 0, 0

    for (opp_move, my_secret_move) in guide:
        my_move = decoder(opp_move, my_secret_move)
        opp_round_score, my_round_score = score(opp_move, my_move)
        opp_score += opp_round_score
        my_score += my_round_score

    return opp_score, my_score


def main(input_file):
    answer_guide = []

    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        answer_guide.append(tuple(line.lower().split()))

    possible_keys = [
        dict(x="a", y="b", z="c"),
        dict(x="a", y="c", z="b"),
        dict(x="b", y="a", z="c"),
        dict(x="b", y="c", z="a"),
        dict(x="c", y="a", z="b"),
        dict(x="c", y="b", z="a"),
    ]

    print(">> part1")
    for i, possible_key in enumerate(possible_keys):
        opp_score, my_score = simulate(
            answer_guide, lambda o, m, poss=possible_key: poss[m]
        )
        print(f"sol {i}: {opp_score=}, {my_score=}")
    print("<< part1")

    print(">> part2")
    opp_score, my_score = simulate(answer_guide, move_for_outcome)
    print(f"{opp_score=}, {my_score=}")
    print("<< part2")


if __name__ == "__main__":
    main(sys.stdin)
