from collections import defaultdict

conversion = {"2": 2, "1": 1, "=": -2, "-": -1, "0": 0}
r_conversion = {v: k for k, v in conversion.items()}


def to_base10(num, _col=1):
    if not num:
        return 0
    return _col * conversion[num[-1]] + to_base10(num[:-1], _col * 5)


def max_digits():
    number = 2
    exp = 0
    while True:
        yield exp, number - 5 ** exp, number
        exp += 1
        number += 2 * 5 ** exp


def _from_base10(num):
    if num == 0:
        return []
    absnum = abs(num)
    for exp, one_digit, two_digit in max_digits():
        if two_digit >= absnum:
            break
    if num > 0:
        if absnum <= one_digit:
            yield (exp, 1)
            yield from _from_base10(num - 5 ** exp)
        else:
            yield (exp, 2)
            yield from _from_base10(num - 2 * 5 ** exp)
    else:
        if absnum <= one_digit:
            yield from _from_base10(num + 5 ** exp)
            yield (exp, -1)
        else:
            yield (exp, -2)
            yield from _from_base10(num + 2 * 5 ** exp)


def from_base10(num):
    digits = defaultdict(int, _from_base10(num))
    return "".join(r_conversion[digits[i]] for i in reversed(range(max(digits)+1)))


total = 0
with open("25.txt") as f:
    for line in f:
        total += to_base10(line.strip())
print(from_base10(total))

