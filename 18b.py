deltas = (
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1)
)


def get_offsets(point):
    return [(x, y, z) for x, y, z in ((x1 + point[0], y1 + point[1], z1 + point[2]) for (x1, y1, z1) in deltas) if min_x-1 <= x <= max_x+1 and min_y-1 <= y <= max_y+1 and min_z-1 <= z <= max_z+1]


with open("18.txt") as f:
    points = {tuple(int(p) for p in line.strip().split(",")) for line in f}

max_x = max(p[0] for p in points)
max_y = max(p[1] for p in points)
max_z = max(p[2] for p in points)
min_x = min(p[0] for p in points)
min_y = min(p[1] for p in points)
min_z = min(p[2] for p in points)

start = (max_x, max_y, max_z)
assert start not in points

outside = {start}
done = set()

while len(done) != len(outside):
    for pos in outside - done:
        done.add(pos)
        for offset in get_offsets(pos):
            if offset not in points:
                outside.add(offset)


surface_area = 0
for point in points:
    surface_area += sum((x1+point[0], y1+point[1], z1+point[2]) in outside for (x1, y1, z1) in deltas)

print(surface_area)
