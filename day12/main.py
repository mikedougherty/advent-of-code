import collections
import pprint
import sys


def main(input_file):
    the_map = collections.defaultdict(set)
    for line in input_file.readlines():
        line = line.strip()
        left, right = line.split('-', 1)
        the_map[left].add(right)
        the_map[right].add(left)
    the_map = dict(the_map.items())

    paths = set([('start',)])
    finished_paths = set()

    pprint.pprint(the_map)

    while paths:
        p = paths.pop()
        if p[-1] == 'end':
            finished_paths.add(p)
            continue

        new_paths = set()
        adjacent = the_map.get(p[-1], set())
        if not adjacent:
            continue

        for adj in adjacent:
            if adj == 'start':
                continue
            if adj == adj.lower() and adj in p:
                continue
            new_paths.add(p + (adj,))

        print(new_paths)
        paths |= new_paths

    pprint.pprint(finished_paths)
    print(f"Found this many paths: {len(finished_paths)}")

if __name__ == "__main__":
    main(sys.stdin)
