from typing import List

with open("20.txt") as f:
    lines = [int(i) for i in f.read().split("\n")]


class Node:
    def __init__(self, value):
        self.value = value
        self.prev: Node = None
        self.next: Node = None

    def __repr__(self):
        return f"<Node value={self.value}>"

    def move(self, amount: int):
        cur = self
        for i in range(abs(amount)):
            if amount > 0:
                cur = cur.next
            else:
                cur = cur.prev
        if cur is self:
            return

        self.prev.next, self.next.prev = self.next, self.prev
        if amount > 0:
            self.next, self.prev = cur.next, cur
        else:
            self.next, self.prev = cur, cur.prev
        self.prev.next = self.next.prev = self


def setup_linked_list(line) -> List[Node]:
    nodes = [Node(i) for i in line]
    for i, j in zip(nodes, nodes[1:]):
        i.next = j
        j.prev = i
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]
    assert all(node.next is not Node for node in nodes)
    assert all(node.prev is not Node for node in nodes)
    return nodes


def get_line(nodes: List[Node]) -> List[int]:
    zero = next(node for node in nodes if node.value[1] == 0)
    cur = zero
    while True:
        #print(cur.prev, cur, cur.next)
        assert cur.next is not None

        yield cur.value[1]
        cur = cur.next
        if cur is zero:
            return


def mix(line):
    linked_list = setup_linked_list(enumerate(line))
    #print(list(get_line(linked_list)))
    for i, value in enumerate(line):
        current_node: Node = next(node for node in linked_list if node.value[0] == i)
        current_node.move(current_node.value[1])
        _line = list(get_line(linked_list))
        print(_line)
        #assert _line == turns[i]
    return list(get_line(linked_list))

lines = mix(lines)
factors = [lines[(i * 1000) % len(lines)] for i in range(1, 4)]
print(factors, sum(factors))
