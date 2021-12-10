import sys

corrupt_score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
    None: 0,
}


autocomplete_score_table = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

ch_pairs = {
    "[": "]",
    "{": "}",
    "(": ")",
    "<": ">",
}


def main(input_file):
    corruption_score = 0
    autocomplete_scores = []
    for line in input_file.readlines():
        autocomplete_score = 0
        line = line.strip()
        stack = []
        for ch in line:
            if ch in ch_pairs:
                # opening a new block
                stack.append(ch)
                continue

            # closing a block, must match last thing on our stack
            if ch_pairs[stack[-1]] == ch:
                stack.pop()
            else:
                corruption_score += corrupt_score_table.get(ch)
                break
        else:
            # Did not break, line is incomplete.
            autocomplete = "".join(ch_pairs.get(ch) for ch in stack[::-1])
            for ch in autocomplete:
                autocomplete_score *= 5
                autocomplete_score += autocomplete_score_table.get(ch)

            autocomplete_scores.append(autocomplete_score)

    autocomplete_scores.sort()
    print(autocomplete_scores)
    final_autocomplete_score = autocomplete_scores[len(autocomplete_scores) // 2]

    print(f"Syntax error score: {corruption_score}")
    print(f"Autocomplete score: {final_autocomplete_score}")


if __name__ == "__main__":
    main(sys.stdin)
