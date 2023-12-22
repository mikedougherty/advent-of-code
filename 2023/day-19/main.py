import dataclasses
import functools
import math
import multiprocessing
import sys

@dataclasses.dataclass
class Part:
    x: int = 0
    m: int = 0
    a: int = 0
    s: int = 0

    @classmethod
    def from_str(cls, s):
        assert s.startswith("{")
        assert s.endswith("}")
        s = s[1:-1]
        fields = {}
        for token in s.split(','):
            field, val = token.split('=')
            val = int(val)
            fields.update({field: val})

        return cls(**fields)


@dataclasses.dataclass
class WorkflowRule:
    destination: str
    condition: str

    def __post_init__(self):
        if self.condition:
            self.field = self.condition[0]
            self.operation = self.condition[1]
            self.target = int(self.condition[2:])

    def apply(self, part):
        if not self.condition:
            return True

        val = getattr(part, self.field)
        if self.operation == '<':
            return val < self.target
        elif self.operation == '>':
            return val > self.target
        raise ValueError(f"Unknown operation: {self.operation}")

    @classmethod
    def from_str(cls, s):
        if ':' not in s:
            return cls(s, '')
        condition, dest = s.split(':')
        return cls(dest, condition)

@dataclasses.dataclass
class Workflow:
    name: str
    rules: list[WorkflowRule]

    @classmethod
    def from_string(cls, s):
        name, s = s.split('{')
        assert s.endswith('}')
        s = s[:-1]
        rules = []
        for token in s.split(','):
            rules.append(WorkflowRule.from_str(token))
        return cls(name, rules)

    def apply(self, part) -> str:
        for rule in self.rules:
            if rule.apply(part):
                return rule.destination

        assert False, f"No rule matched for {part}"

class WorkflowEngine:
    workflows: dict[str, Workflow]

    def __init__(self):
        self.workflows = {}

    def add_workflow(self, line):
        w = Workflow.from_string(line)
        self.workflows[w.name] = w

    def apply(self, part):
        dest: str = 'in'
        while dest not in 'RA':
            dest = self.workflows[dest].apply(part)
        return dest

    def score(self, input):
        part_args, score = input
        return score * (self.apply(Part(*part_args)) == 'A')


def part_intervals(ch_intervals):
    for x_int_start, x_int_sz in ch_intervals['x']:
        for m_int_start, m_int_sz in ch_intervals['m']:
            for a_int_start, a_int_sz in ch_intervals['a']:
                for s_int_start, s_int_sz in ch_intervals['s']:
                    yield (x_int_start, m_int_start, a_int_start, s_int_start), x_int_sz * m_int_sz * a_int_sz * s_int_sz


def main(input_file):
    engine = WorkflowEngine()
    parts = []

    parsing_workflows = True

    for line in input_file.readlines():
        line = line.strip()

        if line and parsing_workflows:
            engine.add_workflow(line)

        elif not line:
            parsing_workflows = False

        else:
            parts.append(Part.from_str(line))

    total = 0
    for part in parts:
        if engine.apply(part) == 'A':
            total += sum(vars(part).values())

    print(total)

    ## Part 2
    ch_segments = {ch: [0, 4000] for ch in 'xmas'}
    all_rules = [r for w in engine.workflows.values() for r in w.rules]
    for rule in all_rules:
        if rule.condition:
            # for 'x<1000' this appends 999 to the list of x segments
            # for 'y>1000' this appends 1000 to the list of y segments
            ch_segments[rule.field].append(rule.target - (1 if rule.operation == '<' else 0))

    for ch in ch_segments:
        ch_segments[ch].sort()

    # Now create the list of interval start points and their sizes
    # so for a list of segments [0, 500, 1500]
    # we get [(0, 500), (500, 1000)]
    ch_intervals = {ch: [(end, end-start) for start, end in zip(ch_segments[ch], ch_segments[ch][1:])] for ch in 'xmas'}

    total = 0
    # Iterate over each set of ranges, creating each different "range combination"
    # instead of iterating over individual values
    i = 0
    print("intervals:")
    for ch in 'xmas':
        print(ch, len(ch_intervals[ch]))
    iterations = functools.reduce(lambda a, b: a * b, [len(v) for v in ch_intervals.values()], 1)
    print(f"Total expected iterations: {iterations}")

    with multiprocessing.Pool(8) as pool:
        for i, score in enumerate(pool.imap_unordered(engine.score, part_intervals(ch_intervals), chunksize=100000)):
            if i % 10000000 == 0:
                print(f"{math.floor(i/iterations * 100)} {i=} {score=} {total=}")
            total += score

    print(total)


if __name__ == "__main__":
    main(sys.stdin)
