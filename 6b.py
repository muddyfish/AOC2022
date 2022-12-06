with open("6.txt") as f:
    data = f.read()
    for i, chars in enumerate(zip(*[data[i:] for i in range(14)]), 14):
        if len(set(chars)) == 14:
            print(i, chars)
            break
