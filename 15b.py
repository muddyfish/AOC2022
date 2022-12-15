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

bound = 4000000


def correct_check(x, y):
    if 0 <= x <= bound and 0 <= y <= bound:
        for sensor in sensors:
            current_dist = abs(x - sensor[0]) + abs(y - sensor[1])
            max_dist = sensor_dists[sensor]
            if current_dist <= max_dist:
                break
        else:
            print(x * 4000000 + y)
            exit()


for (sx, sy), max_dist in sensor_dists.items():
    max_dist += 1
    for i, x in enumerate(range(sx-max_dist, sx)):
        for y in (sy+i, sy-i):
            correct_check(x, y)
    for i, x in enumerate(range(sx, sx+max_dist+1)):
        for y in ((sy+max_dist)-i, (sy-max_dist)+i):
            correct_check(x, y)

