import itertools
import verba.word.endings as endings
from verba.word.inflection_key import InflectionKey as IK

def identify_subgroup(keywords, subgroups):
    for sg in subgroups:
        if sg in keywords:
            return sg
    return 'reg'

def identify_key_and_stem(word, partial_keys, pofs, groups):
    max_ending_len = 0
    key_match = None
    stem = None
    for pk in partial_keys:
        for g in groups:
            key = pk.union(IK(g))
            if key not in endings.endings[pofs]:
                continue

            ending = endings.endings[pofs][key]
            ending_len = len(ending)
            if word[-ending_len:] == ending and ending_len > max_ending_len:
                key_match = key
                stem = word[:-ending_len]
                max_ending_len = ending_len
    
    return (key_match, stem)

def make_inflections(stem, pofs, inflection_keys, self_key):
    if pofs not in endings.endings:
        return {}

    inflections = {}
    for k in inflection_keys:
        ending_key = self_key.union(k)
        if ending_key not in endings.endings[pofs]:
            continue
        inflections[k] = stem + endings.endings[pofs][ending_key] 
    return inflections

def make_key_products(*args):
    prods = itertools.product(*args)
    keys = [IK(*p) for p in prods]
    return keys
    
