import collections
import dataclasses
import itertools
import sys
import typing

@dataclasses.dataclass
class Module:
    name: str
    receivers: list[str]
    outbox: list[bool] = dataclasses.field(default_factory=list)
    state: bool = False

    COUNTERS: typing.ClassVar[dict[bool, int]] = collections.defaultdict(int)
    ALL: typing.ClassVar[dict[str, 'Module']] = {}
    VERBOSE: typing.ClassVar[bool] = False

    def __post_init__(self):
        self.ALL[self.name] = self

    def pulse(self, source: str, signal: bool):
        self.COUNTERS[signal] += 1
        if self.VERBOSE:
            print(f"{source} -{'high' if signal else 'low'}-> {self.name}")

    def process(self):
        if not self.outbox:
            return

        signal = self.outbox.pop(0)
        for receiver in self.receivers:
            Module.ALL[receiver].pulse(self.name, signal)

            if self.name in set(('db', 'tf', 'ln', 'vq')) and signal:
                print(f"{self.name} emits HIGH, presses: {Module.ALL['button'].presses}")
                if self.name == 'ln':
                    ## See note towards end of main(). 'ln' has the longest period so quit
                    ## when we reach it.
                    raise StopIteration

        for receiver in self.receivers:
            Module.ALL[receiver].process()

    @classmethod
    def from_str(cls, s):
        kind_name, receivers = s.split(' -> ')
        receivers = receivers.split(', ')
        if kind_name == 'broadcaster':
            return Broadcast(kind_name, receivers)
        if kind_name.startswith('%'):
            return FlipFlop(kind_name[1:], receivers)
        if kind_name.startswith('&'):
            return Conjunction(kind_name[1:], receivers)

        assert False


class Broadcast(Module):
    def pulse(self, source: str, signal: bool):
        super().pulse(source, signal)
        self.outbox.append(signal)


class Button(Module):
    presses: int = 0

    def pulse(self, source=None, signal=None):
        super().pulse(source, signal)
        self.presses += 1
        # We only send low signals.
        self.outbox.append(False)
        self.process()


class FlipFlop(Module):
    def pulse(self, source: str, signal: bool):
        super().pulse(source, signal)
        if signal:
            # high signal means do nothing
            return
        # Low signal; flip the state.
        # Our new state is also the value of the new signal we're sending.
        # AKA, old_state == True means we're turning off and sending a low signal (False)
        #      old_state == False means we're turning on and sending a high signal (True)
        self.state = not self.state
        self.outbox.append(self.state)

class Conjunction(Module):
    def __post_init__(self):
        super().__post_init__()
        # Conjunctions always start ON
        self.memory = {}

    def pulse(self, source: str, signal: bool):
        super().pulse(source, signal)
        self.memory[source] = signal

        if all(self.memory.values()):
            # All inputs are 'HIGH', send a 'LOW'
            self.outbox.append(False)
        else:
            # At least one 'LOW', send 'HIGH'
            self.outbox.append(True)

class Output(Module):
    def pulse(self, source: str, signal: bool):
        super().pulse(source, signal)
        print(f"{self.name}: {'high' if signal else 'low'}")

class RX(Module):
    def pulse(self, source: str, signal: bool):
        super().pulse(source, signal)

        if not signal:
            raise StopIteration

def main(input_file):
    modules: list[Module] = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue

        modules.append(Module.from_str(line))

    for module in modules:
        if type(module) is Conjunction:
            module.memory = {m.name: False for m in modules if module.name in m.receivers}

    button = Button('button', ['broadcaster'])
    _output = Output('output', [])

    ## Comment this out for part1
    rx = RX('rx', [])

    all_receivers = set(itertools.chain(*[m.receivers for m in modules]))
    for r in all_receivers:
        if r not in Module.ALL:
            # Make a dummy module that receives pulses but does nothing.
            Module(r, [])

    i = 0
    ## Uncomment for part1
    # for _ in range(1000):
    # Comment for part1
    while True:
        i += 1
        try:
            button.pulse()
        except StopIteration:
            break

    print(Module.COUNTERS[False] * Module.COUNTERS[True])
    print(i)


    ## The conjunctions 'db', 'tf', 'ln' and 'vq' are the inputs to a final
    ## conjunction 'tg'. Once the 4 are all active simultaneously, 'tg' emits a LOW
    ## signal which triggers the 'rx' StopIteration. Instead of letting this run
    ## for a long time for them to all coincide, run it long enough to find the
    ## cycle times of each of the 4 inputs (should only take about 1 second),
    ## and then find the least common multiple of those inputs.

    ## $ python main.py < input.txt
    ## tf emits HIGH, presses: 3923
    ## db emits HIGH, presses: 3929
    ## vq emits HIGH, presses: 4007
    ## ln emits HIGH, presses: 4091

    ## as it turns out, these are all prime, so the LCM is just their product

    print(3923 * 3929 * 4007 * 4091)


if __name__ == "__main__":
    main(sys.stdin)
