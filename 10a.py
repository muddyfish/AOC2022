from itertools import chain


def noop():
    yield lambda x: x


def addx(val: int):
    yield lambda x: x
    yield lambda x: x + val


instructions = iter([])
with open("10.txt") as f:
    for line in f.readlines():
        line = line.strip()
        match line.split():
            case ["noop"]:
                instructions = chain(instructions, noop())
            case ["addx", val]:
                instructions = chain(instructions, addx(int(val)))

acc = 1
signal_strengths = 0
for i, inst in enumerate(instructions, 1):
    if i % 40 == 20:
        signal_strengths += i * acc
    acc = inst(acc)

print(signal_strengths)
