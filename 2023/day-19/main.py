import dataclasses
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
    # total = 0
    # for x in range(1, 4001):
    #     for m in range(1, 4001):
    #         for a in range(1, 4001):
    #             print(x, m, a)
    #             for s in range(1, 4001):
    #                 part = Part(x, m, a, s)
    #                 if engine.apply(part) == 'A':
    #                     total += sum(vars(part).values())

    # print(total)



if __name__ == "__main__":
    main(sys.stdin)
