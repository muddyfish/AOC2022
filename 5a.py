import re
from itertools import zip_longest

instructions_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")


def remove_quantity(from_, quantity):
    rtn = columns[from_-1][:quantity]
    del columns[from_-1][:quantity]
    return rtn


def add_to(to, to_move):
    columns[to-1] = [*reversed(to_move), *columns[to-1]]


with open("5.txt") as f:
    raw_model, raw_instructions = f.read().split("\n\n")

    model = [i[1::4] for i in raw_model.split("\n")[:-1]]
    instructions = [map(int, instructions_regex.match(i).groups()) for i in raw_instructions.split("\n")]
    columns = [[i for i in col if i != " "] for col in zip_longest(*model, fillvalue=" ")]

    for quantity, from_, to in instructions:
        to_move = remove_quantity(from_, quantity)
        add_to(to, to_move)
    print("".join(i[0] for i in columns))
