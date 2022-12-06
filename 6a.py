with open("6.txt") as f:
    data = f.read()
    for i in range(len(data)):
        if len(set(data[i:i+4])) == 4:
            print(i+4)
            break

