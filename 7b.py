from collections import defaultdict

nexted_defaultdict = lambda: defaultdict(nexted_defaultdict)
directory_structure = nexted_defaultdict()


def add_file(cwd, structure, filesize, filename):
    if cwd:
        add_file(cwd[1:], structure[cwd[0]], filesize, filename)
    else:
        assert not structure[filename]
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


def get_dir_sizes(directory_structure, cwd):
    total_size = 0
    dirs = {}
    for k, v in directory_structure.items():
        if isinstance(v, int):
            total_size += v
        else:
            dirs_, total_size_ = get_dir_sizes(v, cwd + [k])
            dirs.update(dirs_)
            total_size += total_size_
    dirs["".join("/"+i for i in cwd) or "/"] = total_size
    return dirs, total_size


dirs, _ = get_dir_sizes(directory_structure, [])

sizes = sorted(dirs.values())
total_size = dirs["/"]


for i in sizes:
    if total_size - i <= (70000000 - 30000000):
        print(i)
        break
