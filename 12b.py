import math
from string import ascii_lowercase
heightmap = []

with open("12.txt") as f:
    for y, line in enumerate(f):
        line = line.strip()
        heightmap.append([])
        for x, char in enumerate(line):
            match char:
                case "S":
                    start = (x, y)
                    heightmap[-1].append(0)
                case "E":
                    end = (x, y)
                    heightmap[-1].append(25)
                case _:
                    heightmap[-1].append(ascii_lowercase.index(char))


def adjacent(pos):
    if pos[0] != 0:
        yield (pos[0]-1, pos[1])
    if pos[1] != 0:
        yield (pos[0], pos[1]-1)
    if pos[0] != len(heightmap[0])-1:
        yield (pos[0]+1, pos[1])
    if pos[1] != len(heightmap)-1:
        yield (pos[0], pos[1]+1)


def viable(pos):
    cur_height = heightmap[pos[1]][pos[0]]
    for x, y in adjacent(pos):
        new_height = heightmap[y][x]
        if new_height > cur_height + 1:
            continue
        yield x, y


def bfs(current):
    possible = {current: 0}
    explored = set()
    while current != end:
        for pos in viable(current):
            new_dist = possible[current] + 1
            if heightmap[pos[1]][pos[0]] == 0:
                new_dist = 0
            if possible.get(pos, math.inf) > new_dist:
                explored.discard(pos)
                possible[pos] = new_dist
        explored.add(current)
        #print(explored, possible)
        current = min(((k, v) for k, v in possible.items() if k not in explored), key=lambda i: i[1])[0]
    return possible[current]

print(bfs(start))
