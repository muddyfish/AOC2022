from math import prod
with open("8.txt") as f:
    data = [[int(i) for i in line.strip()] for line in f.readlines()]

maxprod = 0
for i, line in enumerate(data):
    if i == 0 or i == len(data) - 1:
        continue
    for j, pos in enumerate(line):
        if j == 0 or j == len(line) - 1:
            continue
        w, e = [data[k][j] for k in reversed(range(i))], [data[k][j] for k in range(i+1, len(data))]
        n, s = [data[i][k] for k in reversed(range(j))], [data[i][k] for k in range(j+1, len(line))]

        sizes = []
        for sightline in (w, e, n, s):
            for l, p in enumerate(sightline, 1):
                if pos <= p:
                    break
            sizes.append(l)
        maxprod = max(maxprod, prod(sizes))

print(maxprod)