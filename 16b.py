import functools
import itertools
import math
import re
import dataclasses
from typing import List, Set, Dict, Tuple

line_regex = re.compile(r"Valve (.{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)\n?")


@dataclasses.dataclass()
class Valve:
    name: str
    rate: int
    others: List[str]
    dists: Dict[str, int]


valves = {}
with open("16.txt") as f:
    for line in f:
        name, rate, others = line_regex.match(line).groups()
        others = others.split(", ")
        rate = int(rate)
        valves[name] = Valve(name, rate, others, {})


def bfs(current: Valve):
    possible = {current.name: 0}
    explored = set()
    while len(explored) != len(valves):
        current = valves[min(((k, v) for k, v in possible.items() if k not in explored), key=lambda i: i[1])[0]]
        for pos in current.others:
            new_dist = possible[current.name] + 1
            if possible.get(pos, math.inf) > new_dist:
                explored.discard(pos)
                possible[pos] = new_dist
        explored.add(current.name)

    return possible


for node in valves.values():
    node.dists = bfs(node)


@functools.cache
def run(cur: Tuple[int, str], other: Tuple[int, str], closed_valves: Set[str]) -> int:
    totals = [0]
    for valve_name in closed_valves:
        cur_sim = valves[cur[1]].dists[valve_name] + 1
        _time_left = cur[0] - cur_sim
        if _time_left <= 0:
            continue
        flow_gained = _time_left * valves[valve_name].rate

        if _time_left > other[0]:
            totals.append(flow_gained + run((_time_left, valve_name), other, closed_valves - {valve_name}))
        else:
            totals.append(flow_gained + run(other, (_time_left, valve_name), closed_valves - {valve_name}))
    return max(totals)


print(run((26, "AA"), (26, "AA"), frozenset(valve.name for valve in valves.values() if valve.rate)))
