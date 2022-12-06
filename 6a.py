with open("6.txt") as f:
    data = f.read()
    for i, chars in enumerate(zip(data, data[1:], data[2:], data[3:]), 4):
        if len(set(chars)) == 4:
            print(i, chars)
            break

