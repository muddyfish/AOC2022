import json
with open("13.txt") as f:
    packets = [[json.loads(i) for i in pair.split("\n")] for pair in f.read().split("\n\n")]


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
        return True
    except Wrong:
        return False


print(sum(i for i, (p1, p2) in enumerate(packets, 1) if cmp(p1, p2)))
