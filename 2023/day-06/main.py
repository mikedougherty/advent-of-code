import dataclasses
import sys

@dataclasses.dataclass
class Racecourse:
    duration: int
    distance: int

@dataclasses.dataclass
class Trial:
    racecourse: Racecourse
    wait: int
    acceleration: int = 1

    @property
    def speed(self):
        return self.wait * self.acceleration

    @property
    def complete(self):
        return self.racecourse.distance < self.distance

    @property
    def distance(self):
        return (self.racecourse.duration - self.wait) * self.speed


def possible_successes(race):
    successes = 0
    for wait in range(race.duration):
        successes += Trial(race, wait).complete
        
    return successes


def main(input_file):
    times = []
    distances = []

    big_race_time = 0
    big_race_distance = 0
    for line in input_file.readlines():
        line = line.strip()
        if not line: continue

        key, values = line.split(":")
        pt1_values = [int(v) for v in values.split() if v]
        if key == 'Time':
            times = pt1_values
            big_race_time = int(''.join(values.split()))
        elif key == 'Distance':
            distances = pt1_values
            big_race_distance = int(''.join(values.split()))
        
    racecourses = [Racecourse(*x) for x in zip(times, distances)]
    big_racecourse = Racecourse(big_race_time, big_race_distance)
    
    solution = 1
    for race in racecourses:
        solution *= possible_successes(race)

    print(solution)
    print(possible_successes(big_racecourse))


if __name__ == "__main__":
    main(sys.stdin)
