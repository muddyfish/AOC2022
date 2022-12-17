import dataclasses
import itertools
from typing import Tuple, Set

Position = Tuple[int, int]

with open("17.txt") as f:
    chars = f.read()

rocks = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (1, 2), (2, 1)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]

initial_x = 2
max_x = 6
max_height = -1
tower = set()
dirs = {">": (1, 0), "<": (-1, 0)}
down = (0, -1)

rocks_fallen = 0
rocks_iter = itertools.cycle(rocks)


@dataclasses.dataclass
class Rock:
    pieces: Set[Position]
    offset: Position

    def get_pos(self) -> Set[Position]:
        return {(x1+self.offset[0], y1+self.offset[1]) for x1, y1 in self.pieces}

    def collides(self) -> bool:
        places = self.get_pos()
        if not all(0 <= x <= max_x for (x, y) in places):
            return True
        if any(y < 0 for (x, y) in places):
            return True
        if any(pos in tower for pos in places):
            return True
        return False

    def __iadd__(self, other: Position):
        self.offset = (self.offset[0] + other[0], self.offset[1] + other[1])
        return self

    def __isub__(self, other: Position):
        self.offset = (self.offset[0] - other[0], self.offset[1] - other[1])
        return self


def draw_tower():
    for y in range(max_height+6, -1, -1):
        print(f"|{''.join('@' if (x,y) in current_rock.get_pos() else ' #'[(x, y) in tower] for x in range(max_x+1))}|", y)


def add_rock(rock: Rock):
    global max_height
    for (x, y) in rock.get_pos():
        tower.add((x, y))
        max_height = max(max_height, y)


def create_rock() -> Rock:
    pieces = next(rocks_iter)
    initial_pos = (initial_x, max_height + 4)
    return Rock(pieces, initial_pos)


current_rock = create_rock()

period = {}

y_offset = None
offsets = {}
first_repeat = None
repeat_data = None

for i, char in enumerate(itertools.cycle(chars)):
    # Left/right
    offset = dirs[char]
    current_rock += offset
    if current_rock.collides():
        current_rock -= offset

    # Down
    current_rock += down
    if current_rock.collides():
        current_rock -= down
        add_rock(current_rock)
        rocks_fallen += 1
        if rocks_fallen == 1:
            y_offset = current_rock.offset[0]
        if current_rock.pieces == rocks[0] and current_rock.offset[0] == y_offset and max(y for x, y in current_rock.get_pos()) == max_height:
            if first_repeat is None:
                char_offset = i % len(chars)
                if char_offset in offsets:
                    first_repeat = char_offset
                    repeat_data = (rocks_fallen, max_height)
                else:
                    offsets[char_offset] = (rocks_fallen, max_height)
            elif i % len(chars) == first_repeat:
                break
        if first_repeat is not None:
            period[rocks_fallen-repeat_data[0]] = max_height-repeat_data[1]
        current_rock = create_rock()


period_offset = offsets[first_repeat][0]
offset = offsets[first_repeat][1] + 1
multiplier = max_height-repeat_data[1]


def max_height(rocks_fallen) -> int:
    return ((rocks_fallen-period_offset) // len(period)) * multiplier + offset + period[(rocks_fallen-period_offset) % len(period)]


print(max_height(1000000000000))
