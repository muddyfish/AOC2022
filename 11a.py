from dataclasses import dataclass
from typing import List, Callable
import re

number_regex = re.compile(r"(\d+)")
op_regex = re.compile(r"Operation: new = (old . (?:\d+|old|new))")


@dataclass
class Monkey:
    items: List[int]
    operation: Callable[[int], int]
    test: int
    true: int
    false: int
    inspections: int


def convert_op(op):
    return eval(f"lambda old: {op}")


monkeys = []
with open("11.txt") as f:
    for monkey_data in f.read().split("\n\n"):
        _, starting, op, test, true, false = [line.strip() for line in monkey_data.split("\n")]
        starting = [int(i) for i in number_regex.findall(starting)]
        op = convert_op(op_regex.match(op).group(1))
        test = int(number_regex.search(test).group(1))
        true = int(number_regex.search(true).group(1))
        false = int(number_regex.search(false).group(1))
        monkeys.append(Monkey(starting, op, test, true, false, inspections=0))


def run_monkey(monkey: Monkey):
    items = monkey.items[:]
    del monkey.items[:]
    for item in items:
        monkey.inspections += 1
        item = monkey.operation(item) // 3
        if item % monkey.test == 0:
            monkeys[monkey.true].items.append(item)
        else:
            monkeys[monkey.false].items.append(item)


for _ in range(20):
    for monkey in monkeys:
        run_monkey(monkey)

monkeys.sort(key=lambda monkey: monkey.inspections)

print(monkeys[-2].inspections * monkeys[-1].inspections)
