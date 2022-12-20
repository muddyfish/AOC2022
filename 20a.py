from typing import Deque
from collections import deque

with open("20.txt") as f:
    lines = [int(i) for i in f.read().split("\n")]


def rotate_until(deque: Deque, condition):
    while not condition(deque[0]):
        deque.rotate(1)


def mix(line):
    queue = deque(enumerate(line))
    for i, value in enumerate(line):
        rotate_until(queue, lambda node: node[0] == i)
        node = queue.popleft()
        queue.rotate(-value)
        queue.appendleft(node)
    rotate_until(queue, lambda node: node[1] == 0)
    return [node[1] for node in queue]


lines = mix(lines)
print(sum(lines[(i * 1000) % len(lines)] for i in range(1, 4)))
