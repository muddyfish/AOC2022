deltas = (
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1)
)

with open("18.txt") as f:
    points = {tuple(int(p) for p in line.strip().split(",")) for line in f}

surface_area = 0
for point in points:
    surface_area += sum((x1+point[0], y1+point[1], z1+point[2]) not in points for (x1, y1, z1) in deltas)

print(surface_area)