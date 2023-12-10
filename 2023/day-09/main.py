import sys


def detect_patterns(location):
    patterns = [location]
    while not all(p == 0 for p in patterns[-1]):
        pat = [b - a for a, b in zip(patterns[-1][:-1], patterns[-1][1:])]
        patterns.append(pat)

    return patterns

def predict_next(location):
    patterns = detect_patterns(location)
    while len(patterns) > 1:
        delta_pattern = patterns.pop()
        patterns[-1].append(patterns[-1][-1] + delta_pattern[-1])
        patterns[-1].insert(0, patterns[-1][0] - delta_pattern[0])
    
    return patterns[0][0], patterns[0][-1]


def main(input_file):
    locations = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        locations.append([int(x) for x in line.split()])

    next_values = []
    for location in locations:
        next_values.append(predict_next(location))

    print(sum(n for p,n in next_values))
    print(sum(p for p,n in next_values))

if __name__ == "__main__":
    main(sys.stdin)
