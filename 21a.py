import re
line_re = re.compile(r"(\w+): (?:(\d+)|(\w+) (.) (\w+))")

tree = {}

with open("21.txt") as f:
    for line in f:
        match = line_re.match(line.strip())
        name, num, name1, op, name2 = match.groups()
        if num:
            tree[name] = lambda a=int(num): a
        else:
            tree[name] = lambda a=name1, b=op, c=name2: eval(f"{tree[a]()} {b} {tree[c]()}")

print("A")
print(tree["root"]())
