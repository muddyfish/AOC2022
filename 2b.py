win = {0: 2, 3: 0, 6: 1}

total = 0
with open("2.txt") as f:
    for (op, me) in map(str.split, f):
        op_shape = "ABC".index(op)
        me_score = "XYZ".index(me) * 3

        me_shape = (win[me_score] + op_shape) % 3
        total += me_score + 1 + me_shape

print(total)
