import sys

score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
    None: 0,
}

ch_pairs = {
    "[": "]",
    "{": "}",
    "(": ")",
    "<": ">",
}


def first_corrupt_character(line):
    stack = []
    for ch in line:
        if ch in ch_pairs:
            # opening a new block
            stack.append(ch)
        else:
            # closing a block, must match last thing on our stack
            if ch_pairs[stack[-1]] == ch:
                stack.pop()
            else:
                return ch


def main(input_file):
    score = 0
    for line in input_file.readlines():
        score += score_table.get(first_corrupt_character(line.strip()))

    print(f"Syntax error score: {score}")


if __name__ == "__main__":
    main(sys.stdin)
