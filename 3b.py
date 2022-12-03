from string import ascii_letters


def split_3(lines):
    try:
        while True:
            yield next(lines), next(lines), next(lines)
    except StopIteration:
        pass


total = 0

with open("3.txt") as f:
    for a, b, c in split_3(f):
        in_common = set(a) & set(b) & set(c) - {"\n"}
        total += sum(ascii_letters.index(i)+1 for i in in_common)

print(total)
