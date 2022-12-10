import math


def move_head(lines):
    head_pos = [0, 0]
    yield tuple(head_pos)
    for line in lines:
        direction, count = line.strip().split(" ")
        for _ in range(int(count)):
            match direction:
                case "U":
                    head_pos[1] -= 1
                case "D":
                    head_pos[1] += 1
                case "L":
                    head_pos[0] -= 1
                case "R":
                    head_pos[0] += 1
            yield tuple(head_pos)


def move_tail(head_history):
    tail_pos = [0, 0]
    yield tuple(tail_pos)
    for head_pos in head_history:
        abs_x = abs(head_pos[0] - tail_pos[0])
        abs_y = abs(head_pos[1] - tail_pos[1])
        move_x = int(math.copysign(1, head_pos[0] - tail_pos[0]))
        move_y = int(math.copysign(1, head_pos[1] - tail_pos[1]))
        if abs_x > 1:
            tail_pos[0] += move_x
            if abs_y != 0:
                tail_pos[1] += move_y
        elif abs_y > 1:
            tail_pos[1] += move_y
            if abs_x != 0:
                tail_pos[0] += move_x
        yield tuple(tail_pos)


with open("9.txt") as f:
    head = move_head(map(str.strip, f))
    tails = [head]
    for i in range(9):
        tails.append(move_tail(tails[-1]))

    print(len(set(tails[-1])))
