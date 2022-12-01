with open("1.txt") as f:
    elves = sorted(sum(int(i) for i in j.split("\n")) for j in f.read().split("\n\n"))
    print(sum(elves[-3:]))
