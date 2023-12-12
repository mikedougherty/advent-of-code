import cachetools
import re
import sys

@cachetools.cached(cachetools.LRUCache(maxsize=1000))
def count_arrangements(spec, groups, group_cursor):
    if not spec:
        # If we still have groups left and we're at the end of the spec,
        # then we have a valid arrangement if the cursor matches the group length.
        if not groups:
            # Out of groups and spec at the same time: valid arrangement
            return 1
        elif len(groups) == 1 and groups[0] == group_cursor:
            # Last group, matches. done!
            return 1
        else:
            # More than one group or last group doesn't match. invalid arrangement
            return 0
        
    num_arrangements = 0
    
    if spec[0] == '?':
        choices = ['.', '#']
    else:
        choices = [spec[0]]

    for ch in choices:
        # continue or start a grouping
        if ch == '#':
            num_arrangements += count_arrangements(spec[1:], groups, group_cursor + 1)
        elif group_cursor > 0 and groups and groups[0] == group_cursor:
            # desired group length is met. on to the next group
            num_arrangements += count_arrangements(spec[1:], groups[1:], 0)
        elif not group_cursor:
            # not in a group and not at the start of a new one
            num_arrangements += count_arrangements(spec[1:], groups, 0)
        # else: ## ??

    return num_arrangements


def main(input_file):
    short_arrangements = 0
    long_arrangements = 0
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        spec, groups = line.split()
        groups = tuple(map(int, groups.split(',')))
        n = count_arrangements(f'.{spec}.', groups, 0)
        # print(f'{spec} {groups} {n}')
        short_arrangements += n
        long_arrangements += count_arrangements(f'.{"?".join([spec] * 5)}.', groups*5, 0)

    print(short_arrangements)
    print(long_arrangements)


if __name__ == "__main__":
    main(sys.stdin)
