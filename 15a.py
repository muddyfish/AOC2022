import re

digits_re = re.compile(r"-?\d+")


sensor_beacons = []
with open("15.txt") as f:
    for line in f:
        sx, sy, bx, by = map(int, digits_re.findall(line))
        sensor_beacons.append(((sx, sy), (bx, by)))

sensors = set(s for s, b in sensor_beacons)
beacons = set(b for s, b in sensor_beacons)
sensor_dists = {s: abs(s[0]-b[0]) + abs(s[1]-b[1]) for s, b in sensor_beacons}
print(sensor_dists)

min_x = min(s[0]-v for s, v in sensor_dists.items())
max_x = max(s[0]+v for s, v in sensor_dists.items())

y = 2000000

total = 0
for x in range(min_x, max_x+1):
    if x % 100000 == 0:
        print(x)
    if (x, y) in beacons:
        continue
    for sensor in sensors:
        current_dist = abs(x-sensor[0]) + abs(y-sensor[1])
        max_dist = sensor_dists[sensor]
        if current_dist <= max_dist:
            total += 1
            break

print(total)