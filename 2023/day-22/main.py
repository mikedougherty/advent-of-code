import copy
import dataclasses
import typing
import sys

@dataclasses.dataclass(order=True, frozen=True)
class Point3D:
    x: int
    y: int
    z: int

    @classmethod
    def from_str(cls, s):
        x, y, z = map(int, s.split(","))
        return cls(x, y, z)


@dataclasses.dataclass(unsafe_hash=True)
class Brick:
    id: int
    p1: Point3D
    p2: Point3D

    ALL: typing.ClassVar[dict[str, 'Brick']] = {}

    def __post_init__(self):
        self.p1, self.p2 = sorted([self.p1, self.p2])
        self.ALL[self.id] = self

    @classmethod
    def from_str(cls, i, s):
        p1_s, p2_s = s.split("~")
        return cls(i, Point3D.from_str(p1_s), Point3D.from_str(p2_s))

    @property
    def cubes(self):
        return abs(((self.p2.x - self.p1.x)+1) * ((self.p2.y - self.p1.y)+1) * ((self.p2.z - self.p1.z)+1))

    def intersects_any(self, vol):
        min_z, max_z = sorted([self.p1.z, self.p2.z])
        min_y, max_y = sorted([self.p1.y, self.p2.y])
        min_x, max_x = sorted([self.p1.x, self.p2.x])
        for z in range(min_z, max_z+1):
            for y in range(min_y, max_y+1):
                for x in range(min_x, max_x+1):
                    if vol[z][y][x] not in ('.', self.id):
                        return True

        return False


def move_brick(vol, old, new):
    # place a 'null' brick in the old spot
    place_brick(vol, Brick('.', old.p1, old.p2))
    # Take the new coordinates and place the brick there
    old.id = new.id
    old.p1 = new.p1
    old.p2 = new.p2
    place_brick(vol, old)


def drop(vol, brick):
    # Construct a new fake brick...
    for z in range(min(brick.p1.z, brick.p2.z), 0, -1):
        new_brick = Brick(
            brick.id,
            Point3D(brick.p1.x, brick.p1.y, brick.p1.z-1),
            Point3D(brick.p2.x, brick.p2.y, brick.p2.z-1)
        )
        # ... and see if it intersects any others. If it does, we can't drop
        # `brick` any further.
        if new_brick.intersects_any(vol):
            return
        else:
            # otherwise, move it to the new location
            move_brick(vol, brick, new_brick)


def settle(vol, bricks):
    for z in range(len(vol)):
        # Find all bricks at this level
        level_bricks = []
        for brick in bricks:
            if min(brick.p1.z, brick.p2.z) == z:
                level_bricks.append(brick)

        # Drop them as low as they can go
        for brick in level_bricks:
            drop(vol, brick)


def find_nearby(vol, brick):
    min_z, max_z = sorted([brick.p1.z, brick.p2.z])
    min_y, max_y = sorted([brick.p1.y, brick.p2.y])
    min_x, max_x = sorted([brick.p1.x, brick.p2.x])
    bricks_beneath = set()
    bricks_above = set()
    for y in range (min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if vol[min_z-1][y][x] != '.':
                bricks_beneath.add(vol[min_z-1][y][x])
            if vol[max_z+1][y][x] != '.':
                bricks_above.add(vol[max_z+1][y][x])

    return bricks_beneath, bricks_above


def place_brick(vol, brick):
    min_z, max_z = sorted([brick.p1.z, brick.p2.z])
    min_y, max_y = sorted([brick.p1.y, brick.p2.y])
    min_x, max_x = sorted([brick.p1.x, brick.p2.x])
    for z in range(min_z, max_z+1):
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                vol[z][y][x] = brick.id


def num_to_fall(brick, bricks_above, bricks_below):
    fell = []
    falling = [brick.id]

    while falling:
        b = Brick.ALL[falling.pop()]
        fell.append(b.id)
        for above in bricks_above[b.id]:
            if not (bricks_below[above] - (set(falling)|set(fell))):
                # All bricks below 'above' have fallen or are falling.
                falling.append(above)

    fell.remove(brick.id)
    return len(set(fell))


def main(input_file):
    bricks = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        bricks.append(Brick.from_str(len(bricks), line))

    # this is just to mak sure i am calculating volumes correctly...
    for brick in bricks:
        print(brick.cubes, brick)

    # Build a an empty 3-dimensional volume of the space
    vol = []

    # First, calculate the size of our volume by the highest value for all our bricks in each dimension
    global_max_x = max(max(b.p1.x, b.p2.x) for b in bricks)
    global_max_y = max(max(b.p1.y, b.p2.y) for b in bricks)
    global_max_z = max(max(b.p1.z, b.p2.z) for b in bricks)

    # Fill it with 'empty' spots
    for z in range(global_max_z+1, 0, -1):
        vol.insert(0, [])
        for y in range(global_max_y+1):
            vol[0].append(['.' for _ in range(global_max_x+1)])

    # Place a pseudo-brick at the bottom of the volume to represent the ground.
    ground = Brick('-', Point3D(0,0,0), Point3D(global_max_x, global_max_y, 0))
    place_brick(vol, ground)

    # Fill our volume with bricks
    for brick in bricks:
        place_brick(vol, brick)

    # "drop" all our bricks until they touch the ground or the brick beneath it
    settle(vol, bricks)

    # Store relationships between bricks -- those above them, and those below.
    # bricks_above[b.id] shows the bricks above `b`
    # bricks_below[b.id] shows the bricks below `b
    bricks_above = {}
    bricks_below = {}
    for brick in bricks:
        below, above = find_nearby(vol, brick)
        bricks_above[brick.id] = above
        bricks_below[brick.id] = below

    # Figure out how many bricks would fall if each brick was removed.
    fall_count = {brick.id: num_to_fall(brick, bricks_above, bricks_below) for brick in bricks}

    # PART1: bricks are "safe to remove" if no bricks fall. how many are safe?
    print(sum(fall_count[b.id] == 0 for b in bricks))
    # PART2: For each brick, how many bricks would fall if it was removed? add them up, this is the answer.
    print(sum(fall_count.values()))

if __name__ == "__main__":
    main(sys.stdin)
