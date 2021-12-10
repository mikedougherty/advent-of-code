import sys
import collections

DIGITS = {
    # Sorted by length of value
    1: "cf",  # Unique
    7: "acf",  # Unique
    4: "bcdf",  # Unique
    2: "acdeg",
    3: "acdfg",
    5: "abdfg",
    0: "abcefg",
    6: "abdefg",
    9: "abcdfg",
    8: "abcdefg",  # Unique
}


UNIQUES = (1, 4, 7, 8)


def create_decipher_table(ciphertext):
    ciphertext = set(ciphertext)
    digit_table = {}

    for u in UNIQUES:
        for cipher_digit in list(ciphertext):
            if len(DIGITS[u]) == len(cipher_digit):
                # print(f"found {u}")
                digit_table[u] = cipher_digit
                ciphertext.remove(cipher_digit)

    for cipher_digit in list(ciphertext):
        if len(cipher_digit) != len(DIGITS[3]):
            continue

        if (set(digit_table[1]) | set(cipher_digit)) == set(cipher_digit):
            # print(f"found 3 {cipher_digit=}")
            digit_table[3] = cipher_digit
            ciphertext.remove(cipher_digit)
        elif len(set(digit_table[4]) - set(cipher_digit)) == 2:
            # print(f"found 2 {cipher_digit=}")
            digit_table[2] = cipher_digit
            ciphertext.remove(cipher_digit)
        else:
            # print(f"found 5 {cipher_digit=}")
            digit_table[5] = cipher_digit
            ciphertext.remove(cipher_digit)

    for cipher_digit in list(ciphertext):
        if len(cipher_digit) != len(DIGITS[0]):
            continue
        if len(set(cipher_digit) - set(digit_table[5])) == 2:
            # print(f"found 0 {cipher_digit=}")
            digit_table[0] = cipher_digit
            ciphertext.remove(cipher_digit)

    for cipher_digit in list(ciphertext):
        if len(set(cipher_digit) - set(digit_table[4])) == 3:
            # print(f"found 6 {cipher_digit=}")
            digit_table[6] = cipher_digit
            ciphertext.remove(cipher_digit)

    assert len(ciphertext) == 1
    digit_table[9] = ciphertext.pop()

    return dict(("".join(sorted(v)), k) for k, v in digit_table.items())


def decipher(input, output):
    table = create_decipher_table(input)
    return tuple(table["".join(sorted(i))] for i in input), tuple(
        table["".join(sorted(o))] for o in output
    )


def main(input_file):
    entries = [
        tuple(x.split() for x in line.split(" | ", 1))
        for line in input_file.readlines()
    ]

    hits = 0
    result = 0
    for input, output in entries:
        plain_input, plain_output = decipher(input, output)
        print(f"{input} | {output} -> {plain_input} | {plain_output}")

        for target in UNIQUES:
            for digit in plain_output:
                if digit == target:
                    hits += 1

        result += int("".join(map(str, plain_output)))

    print(f"Detected {hits} instances of {UNIQUES}")
    print(f"Sum of all outputs: {result}")


if __name__ == "__main__":
    main(sys.stdin)
