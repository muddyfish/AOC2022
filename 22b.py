import re
from typing import Tuple

Position = Tuple[int, int, int]
dirs_re = re.compile("(\d+)(\w)?")

DIRECTIONS = {
    "R": 0,
    "D": 1,
    "L": 2,
    "U": 3
}
MAPPING = {"R": 1, "L": -1}
GRID_SIZE = 50

LOOKUPS = {
    (1, 0, 3): (0, 3, 0),
    (1, 0, 2): (0, 2, 0),

    (0, 3, 2): (1, 0, 1),
    (0, 3, 1): (2, 0, 1),
    (0, 3, 0): (1, 2, 3),

    (0, 2, 2): (1, 0, 0),
    (0, 2, 3): (1, 1, 0),

    (1, 2, 0): (2, 0, 2),
    (1, 2, 1): (0, 3, 2),

    (1, 1, 0): (2, 0, 3),
    (1, 1, 2): (0, 2, 1),

    (2, 0, 3): (0, 3, 3),
    (2, 0, 0): (1, 2, 2),
    (2, 0, 1): (1, 1, 2),
}


with open("22.txt") as f:
    raw_board, directions = f.read().split("\n\n")
    board = [f" {i} " for i in raw_board.split("\n")]
    board = [" " * len(board[0]), *board, " " * len(board[0])]
    max_x = max(len(row) for row in board)
    board = [row.ljust(max_x, " ") for row in board]


def print_board(position=None):
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if (y, x) == position:
                print("X", end="")
            elif (y, x) in HISTORY:
                print(">v<^"[HISTORY[y, x]], end="")
            else:
                print(col, end="")
        print()


def find_first_x(y):
    return next(i for i, value in enumerate(board[y]) if value != " ")


position = (1, find_first_x(1), 0)
HISTORY = {position[:2]: position[2]}


def _move_grid(position: Position):
    y, x, direction = position
    match direction:
        case 0:
            return y, x + 1
        case 1:
            return y + 1, x
        case 2:
            return y, x - 1
        case 3:
            return y - 1, x


def _get_new_pos(position: Position):
    old_y, old_x, direction = position
    y, x = _move_grid(position)
    if board[y][x] == " ":
        lookup_x = (old_x - 1) // GRID_SIZE
        lookup_y = (old_y - 1) // GRID_SIZE
        new_grid_x, new_grid_y, new_direction = LOOKUPS[lookup_x, lookup_y, direction]
        rel_x = ((old_x - 1) % GRID_SIZE)
        rel_y = ((old_y - 1) % GRID_SIZE)
        new_grid_x *= GRID_SIZE
        new_grid_y *= GRID_SIZE

        if direction in (0, 2):
            changes = rel_y
        else:
            changes = rel_x

        print(direction, new_direction, new_grid_x, new_grid_y, changes)
        match (lookup_x, lookup_y, direction):
            case (1, 0, 3):
                y, x = new_grid_y + changes + 1, new_grid_x + 1
            case (1, 0, 2):
                y, x = new_grid_y+GRID_SIZE-changes, new_grid_x+1

            case (0, 3, 2):
                y, x = new_grid_y + 1, new_grid_x + changes + 1
            case (0, 3, 1):
                y, x = new_grid_y + 1, new_grid_x + changes + 1
            case (0, 3, 0):
                y, x = new_grid_y+GRID_SIZE, new_grid_x+changes+1

            case (0, 2, 2):
                y, x = new_grid_y + GRID_SIZE-changes, new_grid_x + 1
            case (0, 2, 3):
                y, x = new_grid_y + changes + 1, new_grid_x + 1

            case (1, 2, 0):
                y, x = new_grid_y+GRID_SIZE-changes, new_grid_x+GRID_SIZE
            case (1, 2, 1):
                y, x = new_grid_y+changes+1, new_grid_x+GRID_SIZE

            case (1, 1, 0):
                y, x = new_grid_y+GRID_SIZE, new_grid_x+1+changes
            case (1, 1, 2):
                y, x = new_grid_y+1, new_grid_x+changes+1

            case (2, 0, 3):
                y, x = new_grid_y+GRID_SIZE, new_grid_x+changes+1
            case (2, 0, 0):
                y, x = new_grid_y+GRID_SIZE-changes, new_grid_x+GRID_SIZE
            case (2, 0, 1):
                y, x = new_grid_y+changes+1, new_grid_x+GRID_SIZE
            case _:
                raise AssertionError()
        _y, _x = _move_grid((y, x, (new_direction - 2) % 4))
        assert board[_y][_x] == " "
        direction = new_direction
    if board[y][x] == "#":
        raise StopIteration()
    return y, x, direction


def move(position: Position, amount: int) -> Position:
    y, x, direction = position
    try:
        for i in range(amount):
            y, x, direction = _get_new_pos((y, x, direction))
            HISTORY[y, x] = direction
            #print_board((y, x))
    except StopIteration:
        pass
    return y, x, direction


#print_board()
for match in dirs_re.finditer(directions):
    amount, direction = match.groups()
    amount = int(amount)
    position = move(position, amount)
    if direction is None:
        new_direction = position[2]
    else:
        new_direction = (position[2] + MAPPING[direction]) % 4
    position = (position[0], position[1], new_direction)
    #print(position, amount)
    # print_board()
print_board()
print(position)
print(position[0] * 1000 + 4 * position[1] + position[2])



