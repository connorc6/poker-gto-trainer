import itertools
from treys import Card

def rank_index(rank):
    return "23456789TJQKA".index(rank)

def expand_range(shorthand):
    shorthand = shorthand.replace(" ", "")
    tokens = shorthand.split(',')
    all_combos = []

    for token in tokens:
        if '+' in token:
            base = token[:-1]
            if len(base) == 2 and base[0] == base[1]:
                all_combos += expand_pair_plus(base)
            else:
                all_combos += expand_broadway_plus(base)
        elif '-' in token:
            all_combos += expand_range_dash(token)
        else:
            all_combos += expand_exact(token)

    return all_combos

def expand_exact(code):
    suits = ['h', 'd', 'c', 's']
    combos = []

    if len(code) == 2:  # e.g. AK = both suited & offsuit
        high, low = code[0], code[1]
        combos += expand_exact(high + low + 's')
        combos += expand_exact(high + low + 'o')
    elif len(code) == 3:
        r1, r2, suited = code[0], code[1], code[2]
        for s1 in suits:
            for s2 in suits:
                if r1 == r2 and s1 >= s2:
                    continue  # avoid duplicate pairs
                if s1 == s2 and suited == 's':
                    combos.append(f"{r1 + s1} {r2 + s2}")
                elif s1 != s2 and suited == 'o':
                    combos.append(f"{r1 + s1} {r2 + s2}")
    return combos

def expand_pair_plus(pair_str):
    ranks = "23456789TJQKA"
    start = rank_index(pair_str[0])
    return sum([expand_exact(r+r) for r in ranks[start:]], [])

def expand_broadway_plus(code):
    ranks = "23456789TJQKA"
    r1, r2, s = code[0], code[1], code[2]
    start1 = rank_index(r1)
    return sum([expand_exact(r + r2 + s) for r in ranks[start1:]], [])

def expand_range_dash(code):
    ranks = "23456789TJQKA"
    left, right = code.split('-')
    if left[0] == left[1]:  # pair range
        i1, i2 = rank_index(left[0]), rank_index(right[0])
        return sum([expand_exact(r+r) for r in ranks[i1:i2+1]], [])
    else:
        base = left[0]
        start, end = rank_index(left[1]), rank_index(right[1])
        return sum([expand_exact(base + ranks[i] + 's') for i in range(start, end+1)], [])
