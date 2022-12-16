import math
import re
import dataclasses
from typing import List, Set, Dict

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


def run(cur: str, time_left: int, closed_valves: Set[str]) -> int:
    totals = [0]
    for valve_name in closed_valves:
        move_time = valves[cur].dists[valve_name]
        _time_left = time_left - move_time - 1
        if _time_left <= 0:
            continue
        flow_gained = _time_left * valves[valve_name].rate
        totals.append(flow_gained + run(valve_name, _time_left, closed_valves - {valve_name}))
    return max(totals)

print(run("AA", 30, set(valve.name for valve in valves.values() if valve.rate)))
