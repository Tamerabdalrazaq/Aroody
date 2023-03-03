from buhoor import BUHOOR, TAFAEELAT
import json
import itertools


def generat_combinations():
    buhoor_dict = dict()
    for bahr in BUHOOR:
        combinations = set()
        for tafaeela in bahr.tafaaeel:
            if len(combinations) == 0:
                for variant in tafaeela.variants:
                    combinations.add(variant)
            else:
                newcomers = set()
                for combination in combinations:
                    for variant in tafaeela.variants:
                        newcomers.add(combination+variant)
                combinations = list(combination)
        buhoor_dict[bahr.name] = combinations
    return buhoor_dict


def find_tafeela(beats):
    compatiable = []
    for tafaeela in TAFAEELAT:
        if beats in tafaeela:
            compatiable.append(tafaeela)
    return compatiable


def find_compatible_bahr(tafaaeel, partial=False):
    compatible = []
    for bahr in BUHOOR:
        if bahr.is_member(tafaaeel, partial):
            compatible.append(bahr)
    return compatible


def get_composition(beats, rec=False):
    compositions = []
    beats_str = ''.join([str(i) for i in beats])
    find_bahr(beats_str, compositions)
    if len(compositions) > 0:
        return compositions

    if not rec:
        for i in range(7):
            approximations = generate_tone_approximations(beats, i)
            for aprroximation in approximations:
                compositions = get_composition(aprroximation, True)
                if len(compositions) > 0:
                    return compositions
    return []


def find_bahr(beats, compositions, sequence=[]):
    if len(beats) == 0:
        buhur_res = find_compatible_bahr(sequence)
        if len(buhur_res) > 0:
            compositions.append((sequence, buhur_res))
            return
    n = len(beats)
    if n <= 2:
        return
    for i in range(3, min(8, n+1)):
        left, right = beats[:i], beats[i:]
        compatiable = find_tafeela(left)
        for comp in compatiable:
            current_tafaaeel = sequence + [comp]
            if find_compatible_bahr(current_tafaaeel, partial=True):
                find_bahr(right, compositions, current_tafaaeel)


def findsubsets(s, n):
    return list(itertools.combinations(s, n))


def generate_tone_approximations(beats, displacement):
    sakanat = []
    beats_approximations = []
    for h in range(len(beats)):
        if (beats[h] == 0):
            sakanat.append(h)

    for perm in findsubsets(sakanat, displacement):
        clone = beats.copy()
        for k in perm:
            clone[k] = 1
        beats_approximations.append(clone)
    return beats_approximations
