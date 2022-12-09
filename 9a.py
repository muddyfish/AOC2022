import math

head_pos = [0, 0]
tail_pos = [0, 0]

tail_history = set()


def move_head(direction):
    match direction:
        case "U":
            head_pos[1] -= 1
        case "D":
            head_pos[1] += 1
        case "L":
            head_pos[0] -= 1
        case "R":
            head_pos[0] += 1


def move_tail():
    abs_x = abs(head_pos[0] - tail_pos[0])
    abs_y = abs(head_pos[1] - tail_pos[1])
    move_x = int(math.copysign(1, head_pos[0] - tail_pos[0]))
    move_y = int(math.copysign(1, head_pos[1] - tail_pos[1]))
    if abs_x <= 1 and abs_y <= 1:
        return
    if abs_x > 1:
        tail_pos[0] += move_x
        if abs_y != 0:
            tail_pos[1] += move_y
    elif abs_y > 1:
        tail_pos[1] += move_y
        if abs_x != 0:
            tail_pos[0] += move_x
    assert abs(head_pos[0] - tail_pos[0]) <= 1
    assert abs(head_pos[1] - tail_pos[1]) <= 1


tail_history.add(tuple(tail_pos))
with open("9.txt") as f:
    for line in f:
        direction, count = line.strip().split(" ")
        count = int(count)
        for i in range(count):
            move_head(direction)
            move_tail()
            tail_history.add(tuple(tail_pos))
            print(head_pos, tail_pos)


print(len(tail_history))
