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

for char in itertools.cycle(chars):
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
        current_rock = create_rock()

        rocks_fallen += 1
        if rocks_fallen == 2022:
            print(max_height+1)
            break

    assert not current_rock.collides()
