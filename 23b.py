import itertools
from collections import defaultdict

elves = set()

directions = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]

adjacent = {
    ( 0, -1): ((1, -1), ( 0, -1), (-1, -1)),
    ( 0,  1): ((1,  1), ( 0,  1), (-1,  1)),
    (-1,  0): ((-1, 1), (-1,  0), (-1, -1)),
    ( 1,  0): ((1,  1), ( 1,  0), ( 1, -1))
}

all_adjacent = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

with open("23.txt") as f:
    for y, line in enumerate(f):
        elves |= {(x, y) for x, value in enumerate(line) if value == "#"}


def bbox(elves):
    return (
        min(x for x, y in elves),
        min(y for x, y in elves),
        max(x for x, y in elves),
        max(y for x, y in elves),
    )


def pprint(elves):
    x1, y1, x2, y2 = bbox(elves)
    for y in range(y1, y2 + 1):
        for x in range(x1, x2+1):
            print(".#"[(x, y) in elves], end="")
        print()


def create_proposals(elves, directions):
    new_positions = defaultdict(list)
    all_still = True
    for x1, y1 in elves:
        if any((x1+x2, y1+y2) in elves for x2, y2 in all_adjacent):
            for direction in directions:
                if not any((x1+x2, y1+y2) in elves for x2, y2 in adjacent[direction]):
                    new_positions[x1 + direction[0], y1 + direction[1]].append((x1, y1))
                    all_still = False
                    break
            else:
                new_positions[x1, y1].append((x1, y1))
        else:
            new_positions[x1, y1].append((x1, y1))
    return new_positions, all_still


for round in itertools.count(1):
    new_elves = set()
    proposal, all_still = create_proposals(elves, directions)
    if all_still:
        break
    for new_position, pos_elves in proposal.items():
        if len(pos_elves) == 1:
            new_elves.add(new_position)
        else:
            #print(f"{len(pos_elves)} all chose the same position ({new_position}) {pos_elves}")
            new_elves |= set(pos_elves)
    assert len(new_elves) == len(elves)

    #print(f"== End of Round {round} ==")
    #pprint(new_elves)

    elves = new_elves
    directions = [*directions[1:], directions[0]]

print(round)