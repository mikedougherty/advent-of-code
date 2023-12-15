import sys

def aoc_hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256

    return v


def main(input_file):
    print(aoc_hash("HASH"))
    print(aoc_hash("rn=1"))

    input = ''
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        input += line

    print(sum(aoc_hash(p) for p in input.split(',')))

    # Supposedly all python dicts are ordered now, lets take advantage of it
    boxes = [{} for _ in range(256)]
    for cmd in input.split(','):
        if '-' in cmd:
            label = cmd.split('-')[0]
            boxes[aoc_hash(label)].pop(label, None)
        else:
            label, number = cmd.split('=')
            number = int(number)
            boxes[aoc_hash(label)][label] = number

    result = 0
    for i, box in enumerate(boxes):
        for j, (label, number) in enumerate(box.items()):
            result += (i+1) * (j+1) * number

    print(result)


if __name__ == "__main__":
    main(sys.stdin)
