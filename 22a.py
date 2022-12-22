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

with open("22.txt") as f:
    raw_board, directions = f.read().split("\n\n")
    board = [f" {i} " for i in raw_board.split("\n")]
    board = [" " * len(board[0]), *board, " " * len(board[0])]
    max_x = max(len(row) for row in board)
    board = [row.ljust(max_x, " ") for row in board]


def print_board():
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if (y, x) == position[:2]:
                print("X", end="")
            else:
                print(col, end="")
        print()


def find_first_x(y):
    return next(i for i, value in enumerate(board[y]) if value != " ")


def find_first_y(x):
    return next(i for i, value in enumerate(board) if value[x] != " ")


def find_last_x(y):
    return next(i for i, value in reversed(list(enumerate(board[y]))) if value != " ")


def find_last_y(x):
    return next(i for i, value in reversed(list(enumerate(board))) if value[x] != " ")


position = (1, find_first_x(1), 0)


def _get_new_pos(y, x, find, is_x):
    if board[y][x] == " ":
        if is_x:
            x = find(y)
        else:
            y = find(x)
    if board[y][x] == "#":
        raise StopIteration()
    return y, x


def move(position: Position, amount: int, new_direction: int) -> Position:
    y, x, direction = position
    try:
        for i in range(amount):
            match direction:
                case 0:
                    y, x = _get_new_pos(y, x + 1, find_first_x, True)
                case 1:
                    y, x = _get_new_pos(y + 1, x, find_first_y, False)
                case 2:
                    y, x = _get_new_pos(y, x - 1, find_last_x, True)
                case 3:
                    y, x = _get_new_pos(y - 1, x, find_last_y, False)
    except StopIteration:
        pass
    return y, x, new_direction


#print_board()
for match in dirs_re.finditer(directions):
    amount, direction = match.groups()
    print(amount, direction)
    if direction is None:
        new_direction = position[2]
        break
    else:
        new_direction = (position[2] + MAPPING[direction]) % 4
    amount = int(amount)
    position = move(position, amount, new_direction)
    #print(position, amount)
    #print_board()

print(position[0] * 1000 + 4 * position[1] + position[2])



