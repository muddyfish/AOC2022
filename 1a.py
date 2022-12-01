with open("1.txt") as f:
    elves = [sum(int(i) for i in j.split("\n")) for j in f.read().split("\n\n")]
    print(max(elves))
