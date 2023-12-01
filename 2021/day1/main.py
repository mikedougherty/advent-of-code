import sys

def main(window_size, input):
    increases = 0
    buffer = []

    for line in input.readlines():
        val = int(line.strip())
        buffer.append(val)

        if len(buffer) > (1 + window_size):
            buffer.pop(0)

        if len(buffer) < (1 + window_size):
            continue

        if (sum(buffer[:window_size]) < sum(buffer[1:window_size+1])):
            increases += 1

    print(increases)

if __name__ == '__main__':
    main(int(sys.argv[1]), sys.stdin)