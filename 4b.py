import re

regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)" + "\n?")


total = 0
with open("4.txt") as f:
    for i in f:
        a, b, c, d = map(int, regex.match(i).groups())
        if not (b < c or d < a):
            total += 1

print(total)
