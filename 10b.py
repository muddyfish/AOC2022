from itertools import chain

x = 1


def noop():
    yield from [None] * 1


def addx(val: int):
    global x
    yield from [None] * 2
    x += val


instructions = iter([])


with open("10.txt") as f:
    for line in f.readlines():
        line = line.strip()
        match line.split():
            case ["noop"]:
                instructions = chain(instructions, noop())
            case ["addx", val]:
                instructions = chain(instructions, addx(int(val)))


signal_strengths = 0
for i, _ in enumerate(instructions, 1):
    position = i % 40
    if position == 0:
        print()
    else:
        print(".#"[abs(position-1-x) <= 1], end="")

print(signal_strengths)
