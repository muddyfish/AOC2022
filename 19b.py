import math
from math import ceil
from typing import Dict, TypedDict, Tuple, Optional
import re


costs_re = re.compile(r"Each (\w+) robot costs (.+)")
and_re = re.compile(r"(\d+) (\w+)")


class Blueprint(TypedDict):
    ore: Dict[str, int]
    clay: Dict[str, int]
    obsidian: Dict[str, int]
    geode: Dict[str, int]


blueprints = []
with open("19.txt") as f:
    for line in f:
        blueprint = {k: [and_re.search(i).groups() for i in v.split("and")] for k, v in [costs_re.search(line).groups() for line in line.strip().split(".") if line]}
        blueprint = {k: {j: int(i) for i, j in v} for k, v in blueprint.items()}
        blueprints.append(Blueprint(blueprint))


class Solver:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        self.max_costs = {}
        for components in blueprint.values():
            for item, cost in components.items():
                self.max_costs[item] = max(self.max_costs.get(item, 0), cost)
        self._cur_max = 0

    def _get_max(self, time_left: int, items: Dict[str, Tuple[int, int]], item: str, components: Dict[str, int]) -> Optional[int]:
        # Items: [Right now, Per step]
        time_spent = 0
        for component, required in components.items():
            available, per_step = items[component]
            if required > available + per_step * time_left:
                return
            time_spent = max(time_spent, ceil((required - available) / per_step))

        time_spent += 1
        time_left -= time_spent
        if time_left <= 0:
            return
        _items = {component: (available + (per_step * time_spent) - components.get(component, 0), per_step) for component, (available, per_step) in items.items()}
        _items[item] = (_items[item][0], _items[item][1] + 1)

        return self.get_max(time_left, _items)

    def get_max(self, time_left: int, items: Dict[str, Tuple[int, int]]):
        _geode_count = items["geode"][0] + items["geode"][1] * time_left
        if _geode_count > self._cur_max:
            self._cur_max = _geode_count
        for item, components in self.blueprint.items():
            if items[item][1] < self.max_costs.get(item, math.inf):
                # If we've already built more than we can consume per turn, no point building more
                self._get_max(time_left, items, item, components)
        return self._cur_max


total = 1
for i, blueprint in enumerate(blueprints[:3], 1):
    solver = Solver(blueprint)
    geodes = solver.get_max(32, {"ore": (0, 1), "clay": (0, 0), "obsidian": (0, 0), "geode": (0, 0)})
    print(i, geodes)
    total *= geodes
print(total)
