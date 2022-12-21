import re
line_re = re.compile(r"(\w+): (?:(\d+)|(\w+) (.) (\w+))")
match_re = re.compile("^\((\d+(?:.0)?|.+) (.) (\d|.+)\)$")

tree = {}


def run_match(a, b):
    if "input" in a:
        input, value = a, b
        value = b
    else:
        input, value = b, a
    input_value = int(_do_equality(input, value))
    print(input_value)
    print(eval(input.replace("input", str(input_value))), value)


def _do_equality(input: str, value: int):
    if input == "input":
        return value
    input_match = match_re.match(input)
    left, op, right = input_match.groups()
    if "input" in left:
        equation = _get_equation_left(int(float(right)), op, value)
        return _do_equality(left, eval(equation))
    elif "input" in right:
        equation = _get_equation_right(int(float(left)), op, value)
        return _do_equality(right, eval(equation))
    else:
        raise AssertionError()


def _get_equation_right(left, op, right):
    match op:
        case "+":
            return f"{right} - {left}"
        case "-":
            return f"{left} - {right}"
        case "*":
            return f"{right} / {left}"
        case "/":
            return f"{right} * {left}"


def _get_equation_left(left, op, right):
    match op:
        case "+":
            return f"{right} - {left}"
        case "-":
            return f"{left} + {right}"
        case "*":
            return f"{right} / {left}"
        case "/":
            return f"{left} * {right}"


def _run_inner(to_evaluate: str | int):
    if isinstance(to_evaluate, (int, float)):
        return to_evaluate
    elif "input" in to_evaluate:
        return to_evaluate
    else:
        return eval(to_evaluate)


with open("21.txt") as f:
    for line in f:
        match = line_re.match(line.strip())
        name, num, name1, op, name2 = match.groups()
        if name == "humn":
            tree[name] = lambda: f"input"
        elif name == "root":
            tree[name] = lambda a=name1, c=name2: run_match(tree[a](), tree[c]())
        elif num:
            tree[name] = lambda a=int(num): a
        else:
            tree[name] = lambda a=name1, b=op, c=name2: _run_inner(f"({_run_inner(tree[a]())} {b} {_run_inner(tree[c]())})")

print(tree["root"]())
