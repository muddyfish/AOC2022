from itertools import chain


def noop():
    yield lambda x: x


def addx(val: int):
    yield lambda x: x
    yield lambda x: x + val


instructions = iter([])
with open("10.txt") as f:
    for line in f.readlines():
        match line.strip().split():
            case ["noop"]:
                instructions = chain(instructions, noop())
            case ["addx", val]:
                instructions = chain(instructions, addx(int(val)))


acc = 1
for i, inst in enumerate(instructions, 1):
    position = i % 40
    if position == 0:
        print()
    else:
        print(".#"[abs(position-1-acc) <= 1], end="")
    acc = inst(acc)
