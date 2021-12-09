import sys

def process_line(line):
    line = line.strip()
    if not line:
        return None
    vector, magnitude = line.split(maxsplit=1)

    return vector, int(magnitude)

def main(input_file):
    # h-pos, depth, aim
    location = [0, 0, 0]
    for vector, mag in map(process_line, input_file.readlines()):
        if vector == 'forward':
            change = [mag, location[2] * mag, 0]
        elif vector == 'down':
            change = [0, 0, mag]
        elif vector == 'up':
            change = [0, 0, -mag]

        location = [location[0] + change[0], location[1] + change[1], location[2] + change[2]]

    print(f"final location: {location=}")
    print(f"answer (x * y): {location[0]*location[1]}")

if __name__ == '__main__':
    main(sys.stdin)