import itertools
import verba.word.endings as endings
from verba.word.inflection_key import InflectionKey as IK

def identify_subgroup(default_subgroup, keywords, subgroups):
    for sg in subgroups:
        if sg in keywords:
            return sg
    return default_subgroup

def has_ending(word, ending):
    ending_len = len(ending)
    return word[-ending_len:] == ending
 
def identify_key_and_stem(word, id_endings):
    max_ending_len = 0
    key_match = None
    stem = ''
    for ending, key in id_endings.items():
        ending_len = len(ending)
        if has_ending(word, ending) and ending_len > max_ending_len:
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