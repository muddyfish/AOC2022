import json
from functools import cmp_to_key

with open("13.txt") as f:
    packets = [json.loads(i) for i in f.read().split("\n") if i]


class Right(Exception): pass
class Wrong(Exception): pass


def _cmp(p1, p2):
    match (p1, p2):
        case int(i), int(j):
            if i < j:
                raise Right()
            elif i > j:
                raise Wrong()
        case list(_), list(_):
            [_cmp(i, j) for i, j in zip(p1, p2)]
            if len(p1) > len(p2):
                raise Wrong()
            if len(p1) < len(p2):
                raise Right()
        case list(i), int(j):
            return _cmp(i, [j])
        case int(i), list(j):
            return _cmp([i], j)
        case _:
            raise AssertionError("Ran out of cases")


def cmp(p1, p2):
    try:
        _cmp(p1, p2)
    except Right:
        return -1
    except Wrong:
        return 1

packets.append([[2]])
packets.append([[6]])

packets.sort(key=cmp_to_key(cmp))

div_1 = packets.index([[2]]) + 1
div_2 = packets.index([[6]]) + 1

print(div_1 * div_2)
