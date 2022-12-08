with open("8.txt") as f:
    data = [[int(i) for i in line.strip()] for line in f.readlines()]

trees = set()

for func in [lambda i,j: (i,j), lambda i,j: (j,i)]:
    for i, line in enumerate(data):
        maxline = -1
        for j, pos in enumerate(line):
            if maxline < (maxline := max(maxline, pos)):
                trees.add(func(i, j))
        maxline = -1
        for j, pos in reversed(list(enumerate(line))):
            if maxline < (maxline := max(maxline, pos)):
                trees.add(func(i, j))
    data = list(zip(*data))

print(len(trees))