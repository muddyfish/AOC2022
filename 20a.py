from typing import Deque
from collections import deque

with open("20.txt") as f:
    lines = [int(i) for i in f.read().split("\n")]


def setup_deque(line) -> Deque:
    return deque(line)


def rotate_until(deque: Deque, condition):
    while not condition(deque[0]):
        deque.rotate(1)


def mix(line):
    deque = setup_deque(enumerate(line))
    for i, value in enumerate(line):
        rotate_until(deque, lambda node: node[0] == i)
        node = deque.popleft()
        deque.rotate(-value)
        deque.appendleft(node)
        #print([node[1] for node in deque])
    rotate_until(deque, lambda node: node[1] == 0)
    return [node[1] for node in deque]

lines = mix(lines)
factors = [lines[(i * 1000) % len(lines)] for i in range(1, 4)]
print(factors, sum(factors))
