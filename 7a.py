from collections import defaultdict
import json

nexted_defaultdict = lambda: defaultdict(nexted_defaultdict)
directory_structure = nexted_defaultdict()


def add_file(cwd, structure, filesize, filename):
    if cwd:
        add_file(cwd[1:], structure[cwd[0]], filesize, filename)
    else:
        structure[filename] = filesize


with open("7.txt") as f:
    for line in f:
        line = line.strip()
        opcode, second, *rest = line.split(" ", 2)
        match opcode, second, rest:
            case "$", "cd", ["/"]:
                cwd = []
            case "$", "cd", [".."]:
                del cwd[-1]
            case "$", "cd", [directory]:
                cwd.append(directory)
            case "$", "ls", []:
                pass
            case "dir", directory, []:
                pass
            case filesize, filename, []:
                filesize = int(filesize)
                add_file(cwd, directory_structure, filesize, filename)
            case _, _, _:
                raise AssertionError()


def get_big_dirs(directory_structure, cwd):
    total_size = 0
    big_dirs = {}
    for k, v in directory_structure.items():
        if isinstance(v, int):
            total_size += v
        else:
            big_dirs_, total_size_ = get_big_dirs(v, cwd + [k])
            big_dirs.update(big_dirs_)
            total_size += total_size_
    if total_size < 100000:
        big_dirs["".join("/"+i for i in cwd)] = total_size
    return big_dirs, total_size


print(json.dumps(directory_structure, indent=2, sort_keys=True))
big_dirs, _ = get_big_dirs(directory_structure, [])

print(sum(big_dirs.values()))
