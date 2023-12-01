import sys

def common_bits(entries):
    result = [0] * len(entries[0])

    for entry in entries:

        change = [1 if c == '1' else -1 for c in entry]
        result = [x + y for x, y in zip(result, change)]

    most_least = [(1, 0) if c >= 0 else (0, 1) for c in result]
    return list(zip(*most_least))

def read_gauge(lines, idx):
    remaining = lines[:]
    pos = 0
    while len(remaining) > 1 and pos < len(lines[0]):
        bits = common_bits(remaining)[idx]
        remaining = [x for x in remaining if x[pos] == str(bits[pos])]
        pos += 1

    return int(remaining[0], 2)

def main(input_file):
    lines = [x.strip() for x in input_file.readlines()]
    lines = list(filter(None, lines))

    gamma, epsilon = common_bits(lines)
    print(f"{gamma=} {epsilon=}")

    oxygen = read_gauge(lines, 0)
    c02 = read_gauge(lines, 1)

    gamma_decimal = int(''.join(map(str, gamma)), 2)
    epsilon_decimal = int(''.join(map(str, epsilon)), 2)

    print(f'fuel consumption={gamma_decimal * epsilon_decimal}')
    print(f'life support rating={oxygen * c02}')

if __name__ == '__main__':
    main(sys.stdin)