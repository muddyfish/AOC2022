from string import ascii_letters

total = 0

with open("3.txt") as f:
    for line in f:
        line = line.strip()
        a, b = line[:len(line)//2], line[len(line)//2:]
        in_common = set(a) & set(b)
        total += sum(ascii_letters.index(i)+1 for i in in_common)

print(total)
