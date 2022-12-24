from functools import lru_cache
from typing import Dict
from queue import PriorityQueue

winds = {
    (0, 1): [],
    (0, -1): [],
    (1, 0): [],
    (-1, 0): []
}

DIRECTIONS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
R_DIRECTIONS = {v: k for k, v in DIRECTIONS.items()}
MOVE_DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))


INITIAL_POS = END_POS = (0, 0)
WALLS = set()

with open("24.txt") as f:
    data = f.read()
    line_count = data.count("\n")
    for y, line in enumerate(data.split("\n")):
        line = line.strip()
        for x, point in enumerate(line):
            match point:
                case "#":
                    WALLS.add((y-1, x-1))
                case ".":
                    if y == 0:
                        INITIAL_POS = (y-1, x-1)
                    elif y == line_count:
                        END_POS = (y-1, x-1)
                case _:
                    winds[DIRECTIONS[point]].append((y-1, x-1))
    max_y, max_x = y, x


@lru_cache
def get_winds_at_time(time: int) -> Dict:
    current_winds = {}
    for (dy, dx), inner_winds in winds.items():
        for y, x in inner_winds:
            current_winds[(y+dy*time) % (max_y - 1), (x+dx*time) % (max_x - 1)] = R_DIRECTIONS[dy, dx]
    return current_winds


def print_state(time: int, current_pos):
    current_winds = get_winds_at_time(time)
    print(f"MINUTE {time}")
    for y in range(-1, max_y):
        print("".join("E" if (y, x) == current_pos else current_winds.get((y, x), '.#'[(y, x) in WALLS]) for x in range(-1, max_x)))


def get_deltas_at_time(time: int, position):
    current_winds = get_winds_at_time(time)
    rtn = []
    for dy, dx in MOVE_DIRECTIONS:
        if position == INITIAL_POS and (dy, dx) not in ((1, 0), (0, 0)):
            continue
        y, x = position[0] + dy, position[1] + dx
        if (y, x) not in current_winds and (y, x) not in WALLS:
            rtn.append((y, x))
    return rtn


def run_a_star(current, goal, initial_time):
    possible_queue = PriorityQueue()
    possible_queue.put((0, current, initial_time))
    explored = set()
    while not possible_queue.empty():
        _, current, time = possible_queue.get()
        #print_state(time, current)
        #print()
        if (current, time) in explored:
            continue
        explored.add((current, time))

        for possible_next in get_deltas_at_time(time + 1, current):
            if possible_next == goal:
                return time + 1
            if (possible_next, time + 1) in explored:
                continue

            new_priority = (goal[0] - possible_next[0]) + (goal[1] - possible_next[1]) + time + 1
            possible_queue.put((new_priority, possible_next, time + 1))


print(run_a_star(INITIAL_POS, END_POS, 0))
