import copy
import math
from collections import defaultdict
from itertools import count

lines = []
with open("14.txt") as f:
    for line in f:
        line = line.strip().split(" -> ")
        lines.append([tuple(map(int, point.split(","))) for point in line])


grid = set()
top_sand = (500, 0)


def draw(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:
        for y in range(y1, y2+1):
            grid.add((x1, y))
        for y in range(y2, y1+1):
            grid.add((x1, y))
    elif y1 == y2:
        for x in range(x1, x2+1):
            grid.add((x, y1))
        for x in range(x2, x1+1):
            grid.add((x, y1))
    else:
        raise AssertionError("Not straight")


for line in lines:
    for p1, p2 in zip(line, line[1:]):
        draw(p1, p2)


max_y = max(grid, key=lambda p: p[1])[1]
orig_grid = copy.copy(grid)
columns = defaultdict(set)
for x, y in orig_grid:
    columns[x].add(y)


def print_grid(px=0, py=0):
    min_x = min(grid)[0]
    max_x = max(grid)[0]
    min_y = min(grid, key=lambda p: p[1])[1]
    max_y = max(grid, key=lambda p: p[1])[1]
    for y in range(min_y, max_y+1):
        print("".join(" .#"[((x, y) in grid) + ((x, y) in orig_grid)] if (x,y)!=(px,py) else "o" for x in range(min_x, max_x+1)))
    print()


def get_top_points(min_x, max_x, min_y):
    return [min((y for y in columns[x_pos] if y > min_y), default=max_y+2) for x_pos in range(min_x, max_x+1)]


def fall_sand(x, y):
    left, cur, right = get_top_points(x-1, x+1, y)
    if math.isinf(cur):
        return True
    elif y != cur - 1:
        return fall_sand(x, cur-1)
    if left <= cur >= right:
        grid.add((x, cur-1))
        columns[x].add(cur-1)
        return False
    elif left > cur:
        return fall_sand(x-1, cur)
    elif cur < right:
        return fall_sand(x+1, cur)


for i in count():
    if top_sand in grid:
        break
    if fall_sand(*top_sand):
        break
    if i % 100 == 0:
        print(i)
    #print_grid()

print(i)
