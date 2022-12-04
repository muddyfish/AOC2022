import re

regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)" + "\n?")


total = 0
with open("4.txt") as f:
    for i in f:
        a, b, c, d = map(int, regex.match(i).groups())
        if a <= c and b >= d:
            total += 1
        elif c <= a and d >= b:
            total += 1

print(total)
