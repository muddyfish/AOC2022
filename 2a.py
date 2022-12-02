win = {
    -2: 6,
    -1: 0,
    0: 3,
    1: 6,
    2: 0
}

total = 0
with open("2.txt") as f:
    for (op, me) in map(str.split, f):
        op_shape = "ABC".index(op)
        me_shape = "XYZ".index(me)
        total += win[me_shape - op_shape] + 1 + me_shape

print(total)
