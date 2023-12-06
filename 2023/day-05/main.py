import dataclasses
import cachetools
import multiprocessing
import sys
import typing

MAP_KEY_PARTS = ('seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location')


def make_extended_seed_set(seeds) -> typing.Generator[int, None, None]:
    for start, length in sorted(zip(seeds[:-1:2], seeds[1::2]), key=lambda x: x[1]):
        yield from range(start, start+length)
        print(f"range complete: {start=}, {length=}")

    print("done iterating ranges")

def get_mapped_value(ranges, value):
    for dst, src, length in ranges:
        delta = value - src
        if delta < 0:
            continue
        if delta >= length:
            continue
        return dst + delta
    
    return value


@dataclasses.dataclass
class State:
    input_state : dict

    def find_lowest_location(self, seed_set: typing.Iterable[int]) -> int:
        lowest_location = None
        for seed in seed_set:
            n = self.location(seed)

            if lowest_location is None or n < lowest_location:
                lowest_location = n
        return lowest_location if lowest_location is not None else -1

    def location(self, seed: int) -> int:
        n = seed
        for src, dst in zip(MAP_KEY_PARTS[:-1], MAP_KEY_PARTS[1:]):
            n = get_mapped_value(self.input_state[f"{src}-to-{dst}"], n)
        return n


def main(input_file: typing.TextIO):
    lines = input_file.readlines()

    input_state = {}
    current_map = None
    
    while lines:
        line = lines.pop(0).strip()
        if not line:
            current_map = None
            continue

        if line.endswith(':'):
            assert current_map is None
            name, *rest = line[:-1].split()
            if rest:
                assert(rest[0] == 'map')
            current_map = name
            input_state[current_map] = []

        elif ':' in line:
            assert current_map is None
            name, values = line.split(':')
            input_state[name.strip()] = [int(v.strip()) for v in values.split()]

        else:
            assert current_map is not None
            input_state[current_map].append([int(v) for v in line.split()])
        
    s = State(input_state)
    for seed_set in (iter(input_state['seeds']), make_extended_seed_set(input_state['seeds'])):
        with multiprocessing.Pool(8) as pool:
            lowest_location = None
            for i, loc in enumerate(pool.imap_unordered(s.location, seed_set, chunksize=1000)):
                if i % 1000000 == 0:
                    print(f"{i=} {loc=} {lowest_location=}")

                if lowest_location is None or loc < lowest_location:
                    lowest_location = loc

        print(lowest_location)


if __name__ == "__main__":
    main(sys.stdin)
