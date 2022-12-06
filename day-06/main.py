import sys


def find_header(s, sz):
    window = []
    for i, ch in enumerate(s):
        window.append(ch)
        if len(window) > sz:
            window.pop(0)

        # If N unique characters in an N-sized window... success
        if len(set(window)) == sz:
            return i + 1


def main(input_file):
    lines = []
    for line in input_file.readlines():
        line = line.strip()
        if line:
            lines.append(line)

    for line in lines:
        print("packet start:", find_header(line, 4), line)
        print("message start:", find_header(line, 14), line)


if __name__ == "__main__":
    main(sys.stdin)
