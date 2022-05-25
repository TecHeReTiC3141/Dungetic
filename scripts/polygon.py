def to_base(n, base):
    res = ''
    while n:
        res = str(n % base) + res
        n //= base
    return res

print(to_base(3 ** 14 + 3 ** 8 - 5, 3))